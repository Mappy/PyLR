# -*- coding: utf-8 -*-
''' Location parser 

    .. moduleauthor:: David Marteau <david.marteau@mappy.com>

'''

from __future__ import absolute_import
from base64 import b64decode
from collections import namedtuple
from bitstring import BitStream
from .utils import lazyproperty
from .constants import (LATEST_BINARY_VERSION,
                        BINARY_VERSION_2,
                        MIN_BYTES_LINE_LOCATION,
                        MIN_BYTES_POINT_LOCATION,
                        MIN_BYTES_CLOSED_LINE_LOCATION,
                        MIN_BYTES_POLYGON,
                        RELATIVE_COORD_SIZE,
                        IS_POINT,
                        HAS_ATTRIBUTES,
                        GEOCOORD_SIZE,
                        POINT_ALONG_LINE_SIZE,
                        POINT_WITH_ACCESS_SIZE,
                        POINT_OFFSET_SIZE,
                        AREA_CODE_CIRCLE,
                        AREA_CODE_RECTANGLE,
                        AREA_CODE_POLYGON,
                        RECTANGLE_SIZE,
                        LARGE_RECTANGLE_SIZE,
                        GRID_SIZE,
                        LARGE_GRID_SIZE,
                        LRP_SIZE,
                        CIRCLE_BASE_SIZE,
                        LocationType)
from six.moves import range


class BinaryParseError(Exception):
    pass


class BinaryVersionError(BinaryParseError):
    pass


class InvalidDataSizeError(BinaryParseError):
    pass


# The Constant RFU (Reserved for Future Use)
RFU_BITS = 'uint:1'

# number of bits used for attributes flag
ATTR_FLAG_BITS = 'uint:1'

# number of bits used for point flag
POINT_FLAG_BITS = 'uint:1'

# number of bits used for version
VERSION_BITS = 'uint:3'

AREA_FLAG_BIT0 = 'uint:1'

AREA_FLAG_BIT1 = 'uint:1'

HEADER_BITS = (RFU_BITS,
               ATTR_FLAG_BITS,
               POINT_FLAG_BITS,
               AREA_FLAG_BIT1,
               POINT_FLAG_BITS,
               VERSION_BITS)


_BinaryHeader = namedtuple('_BinaryHeader', ('arf', 'af', 'pf', 'ver'))


class _RawBinaryData(object):
    """ Hold a location reference description as a bit stream."""

    MIN_VERSION = BINARY_VERSION_2
    MAX_VERSION = LATEST_BINARY_VERSION

    
    def __init__(self, data, base64=False):
        """ Constructor.
        
            :param string data: Binaray data
            :param bool base64: True if data is coded in base64
        """
        if base64:
            data = b64decode(data)
        
        #: raw data size
        self._sz = len(data)
        
        #: bit stream used to read data
        self._bs = BitStream(bytes=data)

    def getbits(self, *bits):
        """ Read the given numbers of bits.
        
            :param tuple bits: Tuple of number of bits to read
            :returns: Tuple of bit fields
            :rtype: tuple
        """
        return tuple(self._bs.read(v) for v in bits)
    
    def get_position(self):
        """ Returns position in the bit stream.
        
            :returns: Position in the bit stream
            :rtype: int
        """
        return self._bs.pos

    @property
    def num_bytes(self):
        """ Size of the decoded data.
        
            :returns: Size of the decoded data.
            :rtype: int
        """
        return self._sz

    @property
    def version(self):
        """ Return binary version of the data
        
            :returns: Binary version of the data.
            :rtype: int
        """
        return self.header.ver

    @lazyproperty
    def header(self):
        """ Parse header (once) location type
        
            :returns: Header data
            :rtype: _BinaryHeader
        """
        # Validate data size
        if self._sz < min(MIN_BYTES_LINE_LOCATION,
                          MIN_BYTES_POINT_LOCATION,
                          MIN_BYTES_CLOSED_LINE_LOCATION):
            raise InvalidDataSizeError("not enough bytes in data")

        _, arf1, pf, arf0, af, ver = self.getbits(*HEADER_BITS)
        arf = 2 * arf1 + arf0

        return _BinaryHeader(arf, af, pf, ver)

    @lazyproperty
    def location_type(self):
        """ Parse location type (once)
        
            :returns: Location type
            :rtype: LocationType
        """
        header = self.header

        # Check version
        if not self.MIN_VERSION <= header.ver <= self.MAX_VERSION:
            raise BinaryVersionError("Invalid binary version {}".format(header.ver))

        is_point = (header.pf == IS_POINT)
        has_attributes = (header.af == HAS_ATTRIBUTES)
        area_code = header.arf
        is_area = ((area_code == 0 and not is_point and not has_attributes) or area_code > 0)

        total_bytes = self._sz

        loc_type = LocationType.UNKNOWN

        if not is_point and not is_area and has_attributes:
            loc_type = LocationType.LINE_LOCATION
        elif is_point and not is_area:
            if not has_attributes:
                if total_bytes == GEOCOORD_SIZE:
                    loc_type = LocationType.GEO_COORDINATES
                else:
                    raise InvalidDataSizeError("Invalid byte size")
            else:
                if total_bytes == POINT_ALONG_LINE_SIZE or total_bytes == (POINT_ALONG_LINE_SIZE + POINT_OFFSET_SIZE):
                    loc_type = LocationType.POINT_ALONG_LINE
                elif total_bytes == POINT_WITH_ACCESS_SIZE or total_bytes == (POINT_WITH_ACCESS_SIZE + POINT_OFFSET_SIZE):
                    loc_type = LocationType.POI_WITH_ACCESS_POINT
                else:
                    raise InvalidDataSizeError("Invalid byte size")
        elif is_area and not is_point and has_attributes:
            if total_bytes >= MIN_BYTES_CLOSED_LINE_LOCATION:
                loc_type = LocationType.CLOSED_LINE
            else:
                raise InvalidDataSizeError("Invalid byte size")
        else:
            if area_code == AREA_CODE_CIRCLE:
                loc_type = LocationType.CIRCLE
            elif area_code == AREA_CODE_RECTANGLE:
                # includes case AREA_CODE_GRID
                if total_bytes == RECTANGLE_SIZE or total_bytes == LARGE_RECTANGLE_SIZE:
                    loc_type = LocationType.RECTANGLE
                elif total_bytes == GRID_SIZE or total_bytes == LARGE_GRID_SIZE:
                    loc_type = LocationType.GRID
                else:
                    raise InvalidDataSizeError("Invalid byte size")
            elif area_code == AREA_CODE_POLYGON:
                if not has_attributes and total_bytes >= MIN_BYTES_POLYGON:
                    loc_type = LocationType.POLYGON
                else:
                    raise InvalidDataSizeError("Invalid byte size")
            else:
                raise BinaryParseError('Invalid header')

        return loc_type


def init_binary_parsing(data, base64=False):
    """ Create an instance of _RawBinaryData
        The returned object can be passed to 'parse_binary'
        
        :param string data: string describing the location
        :param bool base64: True if encoded in base 64
        :returns: Parsable data structure
        :rtype: _RawBinaryData
    """
    return _RawBinaryData(data, base64)


def parse_binary(data, base64=False):
    """ Parse binary data.
        Input is original data or an object returned by init_binary_parsing(...)
        
        :param data: string (encoded or not) describing the location
        :param bool base64: True if encoded in base 64
        :returns: Object describing the parsed location, or an error object
    """
    if not isinstance(data, _RawBinaryData):
        data = _RawBinaryData(data, base64)

    # Get header
    loc_type = data.location_type
    
    if loc_type == LocationType.LINE_LOCATION:
        return parse_line(data)
    elif loc_type == LocationType.POINT_ALONG_LINE:
        return parse_point_along_line(data)
    elif loc_type == LocationType.GEO_COORDINATES:
        return parse_geo_coordinates(data)
    elif loc_type == LocationType.POI_WITH_ACCESS_POINT:
        return parse_poi_with_access_point(data)
    elif loc_type == LocationType.RECTANGLE:
        return parse_rectangle(data)
    elif loc_type == LocationType.CLOSED_LINE:
        return parse_closed_line(data)
    elif loc_type == LocationType.CIRCLE:
        return parse_circle(data)
    elif loc_type == LocationType.GRID:
        return parse_grid(data)
    elif loc_type == LocationType.POLYGON:
        return parse_polygon(data)
    else:
        return BinaryParseError("Invalid location type")

# ----------------
# Location parsers
# ----------------

HEAD_FIELDS = ('version', 'type')

from .binary import (_parse_first_lrp,
                     _parse_intermediate_lrp,
                     _parse_last_line_lrp,
                     _parse_last_closed_line_attrs,
                     _parse_offset,
                     _parse_relative_coordinates,
                     _parse_absolute_coordinates,
                     _parse_radius,
                     _parse_grid_dimensions)


# LINE_LOCATION
LineLocation = namedtuple('LineLocation',  HEAD_FIELDS+('flrp', 'llrp', 'points', 'poffs', 'noffs'))
""" Line Location type
"""

def parse_line(rb):
    """ Parse line location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Line location
        :rtype: LineLocation
    """
    assert rb.location_type == LocationType.LINE_LOCATION

    # number of intermediates points
    num_intermediates = (rb.num_bytes - MIN_BYTES_LINE_LOCATION) // LRP_SIZE
    flrp = _parse_first_lrp(rb)

    points = []

    rel = flrp
    for _ in range(num_intermediates):
        ilrp = _parse_intermediate_lrp(rb, rel)
        points.append(ilrp)
        rel = ilrp

    llrp, pofff, nofff = _parse_last_line_lrp(rb, rel)
    poffs = _parse_offset(rb) if pofff else 0
    noffs = _parse_offset(rb) if nofff else 0

    return LineLocation(rb.version, rb.location_type, flrp, llrp, points, poffs, noffs)


# POINT_ALONG_LINE
PointAlongLineLocation = namedtuple('PointAlongLineLocation',  HEAD_FIELDS+('flrp', 'llrp', 'poffs'))
""" Point along location type
"""

def parse_point_along_line(rb):
    """ Parse point along line location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Point along line location
        :rtype: PointAlongLineLocation
    """
    assert rb.location_type == LocationType.POINT_ALONG_LINE

    flrp = _parse_first_lrp(rb)
    llrp, pofff, _ = _parse_last_line_lrp(rb, flrp)
    poffs = _parse_offset(rb) if pofff else 0

    return PointAlongLineLocation(rb.version, rb.location_type, flrp, llrp, poffs)


# GEO_COORDINATES
GeoCoordinateLocation = namedtuple('GeoCoordinateLocation',  HEAD_FIELDS+('coords',))
""" Coordinate location type
"""

def parse_geo_coordinates(rb):
    """ Parse geo coordinates location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Geographic coordinates location
        :rtype: GeoCoordinateLocation
    """
    assert rb.location_type == LocationType.GEO_COORDINATES

    coords = _parse_absolute_coordinates(rb)

    return GeoCoordinateLocation(rb.version, rb.location_type, coords)


# POI_WITH_ACCESS_POINT
PoiWithAccessPointLocation = namedtuple('PoiWithAccessPointLocation',  HEAD_FIELDS+(
    'flrp', 'llrp', 'poffs', 'coords'))
""" Poi with access location type
"""

def parse_poi_with_access_point(rb):
    """ Parse POI with access point
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: POI with access point location
        :rtype: PoiWithAccessPointLocation
    """
    assert rb.location_type == LocationType.POI_WITH_ACCESS_POINT

    flrp = _parse_first_lrp(rb)
    llrp, pofff, _ = _parse_last_line_lrp(rb, flrp)
    poffs = _parse_offset(rb) if pofff else 0
    coords = _parse_relative_coordinates(rb, flrp.coords)

    return PoiWithAccessPointLocation(rb.version, rb.location_type, flrp, llrp,
                                      poffs, coords)


# CIRCLE
CircleLocation = namedtuple('CircleLocation', HEAD_FIELDS+('coords', 'radius'))
""" Circle Location type
"""


def parse_circle(rb):
    """ Parse circle location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Circle location
        :rtype: CircleLocation
    """
    assert rb.location_type == LocationType.CIRCLE

    radius_size = rb.num_bytes - CIRCLE_BASE_SIZE
    
    coords = _parse_absolute_coordinates(rb)
    radius = _parse_radius(rb, radius_size)
    
    return CircleLocation(rb.version, rb.location_type, coords, radius)


# RECTANGLE

BBox = namedtuple('BBox', ('minx', 'miny', 'maxx', 'maxy'))

RectangleLocation = namedtuple('RectangleLocation',  HEAD_FIELDS+('bbox',))
""" Rectangle Location type
"""

def parse_rectangle(rb):
    """ Parse rectangle location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Rectangle location
        :rtype: RectangleLocation
    """
    assert rb.location_type == LocationType.RECTANGLE

    bl = _parse_absolute_coordinates(rb)
    if rb.num_bytes == LARGE_RECTANGLE_SIZE:
        tr = _parse_absolute_coordinates(rb)
    else:
        tr = _parse_relative_coordinates(rb, bl)

    bbox = BBox(bl.lon, bl.lat, tr.lon, tr.lat)

    return RectangleLocation(rb.version, rb.location_type, bbox)


# GRID
GridLocation = namedtuple('GridLocation',  HEAD_FIELDS+('bbox', 'cols', 'rows'))
""" Grid Location type
"""

def parse_grid(rb):
    """ Parse grid location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Grid location
        :rtype: GridLocation
    """
    assert rb.location_type == LocationType.GRID

    bl = _parse_absolute_coordinates(rb)
    if rb.num_bytes == LARGE_GRID_SIZE:
        tr = _parse_absolute_coordinates(rb)
    else:
        tr = _parse_relative_coordinates(rb, bl)

    bbox = BBox(bl.lon, bl.lat, tr.lon, tr.lat)

    cols, rows = _parse_grid_dimensions(rb)

    return GridLocation(rb.version, rb.location_type, bbox, cols, rows)


# CLOSED LINE
ClosedLineLocation = namedtuple('ClosedLineLocation',  HEAD_FIELDS+('flrp', 'points', 'frc', 'fow', 'bear'))

def parse_closed_line(rb):
    """ Parse closed line location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Closed line location
        :rtype: ClosedLineLocation
    """
    assert rb.location_type == LocationType.CLOSED_LINE

    # number of intermediates points
    num_intermediates = (rb.num_bytes - MIN_BYTES_CLOSED_LINE_LOCATION) // LRP_SIZE
    flrp = _parse_first_lrp(rb)
    
    points = []

    rel = flrp
    for _ in range(num_intermediates):
        ilrp = _parse_intermediate_lrp(rb, rel)
        points.append(ilrp)
        rel = ilrp

    frc, fow, bear = _parse_last_closed_line_attrs(rb)
    
    return ClosedLineLocation(rb.version, rb.location_type, flrp, points, frc, fow, bear)


# CLOSED LINE
PolygonLocation = namedtuple('PolygonLocation',  HEAD_FIELDS+('points',))

def parse_polygon(rb):
    """ Parse polygon location
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Polygon location
        :rtype: PolygonLocation
    """
    assert rb.location_type == LocationType.POLYGON

    # number of points
    # MIN_BYTES_POLYGON include first point and 2 relatives points
    num_intermediates = 2 + (rb.num_bytes - MIN_BYTES_POLYGON) // RELATIVE_COORD_SIZE
    points = []

    rel = _parse_absolute_coordinates(rb)
    points.append(rel)
    for _ in range(num_intermediates):
        ilrp = _parse_relative_coordinates(rb, rel)
        points.append(ilrp)
        rel = ilrp

    return PolygonLocation(rb.version, rb.location_type, points)
