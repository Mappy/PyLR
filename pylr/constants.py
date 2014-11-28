# -*- coding: utf-8 -*-
''' Constante definitions

    .. moduleauthor:: David Marteau <david.marteau@mappy.com>
'''


from .utils import enum

''' The data format IDENTIFIER. '''
IDENTIFIER = "binary"


''' The Constant BITS_PER_BYTE. '''
BITS_PER_BYTE = 8

'''
The Constant DECA_MICRO_DEG_FACTOR is used to transform degree values
into deca-micro degrees.
'''
DECA_MICRO_DEG_FACTOR = 100000.0

'''
The Constant BIT24FACTOR is used for the conversion of lat/lon
coordinates into a 24bit accuracy.
'''
BIT24FACTOR = 46603.377778

'''
The Constant BIT24FACTOR_REVERSED is used for the conversion of 24bit
lat/lon values back into prior accuracy.
'''
BIT24FACTOR_REVERSED = 1 / BIT24FACTOR

''' The BEARING_SECTOR defines the length of a bearing interval. '''
BEARING_SECTOR = 11.25

''' The LENGTH_INTERVAL defines the length of a dnp and offset interval. '''
LENGTH_INTERVAL = 58.6

''' The IS_POINT defines a polocation reference. '''
IS_POINT = 1

''' The IS_NOT_POINT indicates that the location reference is not a polocation. '''
IS_NOT_POINT = 0

''' The IS_AREA defines an area location reference. '''
IS_AREA = 1

'''  The AREA_CODE_CIRCLE defines the code for a cirle location reference. '''
AREA_CODE_CIRCLE = 0

'''  The AREA_CODE_RECTANGLE defines the code for a rectangle location reference. '''
AREA_CODE_RECTANGLE = 2

'''  The AREA_CODE_GRID defines the code for a grid location reference. '''
AREA_CODE_GRID = 2  # for BINARY_VERSION_3 the same as for AREA_CODE_RECTANGLE

'''  The AREA_CODE_POLYGON defines the code for a polygon location reference. '''
AREA_CODE_POLYGON = 1

'''  The AREA_CODE_CLOSEDLINE defines the code for a closed line location reference. '''
AREA_CODE_CLOSEDLINE = 3

'''  The AREA_CODE_NOAREA defines the code for a non-area location reference. '''
IS_NOT_AREA = 0

''' The HAS_ATTRIBUTES the existence of attribute information in the stream. '''
HAS_ATTRIBUTES = 1

''' The Constant HAS_NO_ATTRIBUTES. '''
HAS_NO_ATTRIBUTES = 0

''' The HEADER_SIZE defines the size [in bytes] of the header. '''
HEADER_SIZE = 1

'''
The FIRST_LRP_SIZE defines the size [in bytes] of the first location
reference point.
'''
FIRST_LRP_SIZE = 9

'''
The LRP_SIZE defines the size [in bytes] of an intermediate location
reference point.
'''
LRP_SIZE = 7

'''
The LAST_LRP_SIZE defines the size [in bytes] of the last location
reference point.
'''
LAST_LRP_SIZE = 6

''' The Constant ABS_COORD_SIZE. '''
ABS_COORD_SIZE = 6

''' The Constant RELATIVE_OFFSET_LENGTH. '''
RELATIVE_OFFSET_LENGTH = 0.390625

'''
The MIN_BYTES defines the minimum size [in bytes] of a binary location
reference.
'''
MIN_BYTES_LINE_LOCATION = HEADER_SIZE + FIRST_LRP_SIZE + LAST_LRP_SIZE

'''
The MIN_BYTES defines the minimum size [in bytes] of a binary closed line location
reference.
'''
MIN_BYTES_CLOSED_LINE_LOCATION = HEADER_SIZE + FIRST_LRP_SIZE + 2

''' The Constant GEOCOORD_SIZE. '''
GEOCOORD_SIZE = HEADER_SIZE + ABS_COORD_SIZE

''' The Constant MIN_BYTES_POINT_LOCATION. '''
MIN_BYTES_POINT_LOCATION = GEOCOORD_SIZE

''' The Constant BINARY_VERSION_2. '''
BINARY_VERSION_2 = 2

''' The Constant BINARY_VERSION_3. '''
BINARY_VERSION_3 = 3

''' The LATEST_BINARY_VERSION defines the current version of the binary format. '''
LATEST_BINARY_VERSION = BINARY_VERSION_3

''' The HAS_OFFSET defines the existence of offset information. '''
HAS_OFFSET = 1

''' The Constant OFFSET_BUCKETS. '''
OFFSET_BUCKETS = 256

''' The Constant POINT_ALONG_LINE_SIZE. '''
POINT_ALONG_LINE_SIZE = HEADER_SIZE + FIRST_LRP_SIZE + LAST_LRP_SIZE

''' The Constant RELATIVE_COORD_SIZE. '''
RELATIVE_COORD_SIZE = 4

''' number of bits used for a small radius '''
SMALL_RADIUS_BITS = 8

''' number of bits used for a medium radius '''
MEDIUM_RADIUS_BITS = 16

''' number of bits used for a large radius '''
LARGE_RADIUS_BITS = 24

''' number of bits used for a small radius '''
EXTRA_LARGE_RADIUS_BITS = 32

''' The Constant DIMENSION_SIZE. '''
DIMENSION_SIZE = 2

''' The Constant RECTANGLE_SIZE. '''
RECTANGLE_SIZE = HEADER_SIZE + ABS_COORD_SIZE + RELATIVE_COORD_SIZE

''' The Constant LARGE_RECTANGLE_SIZE. '''
LARGE_RECTANGLE_SIZE = HEADER_SIZE + ABS_COORD_SIZE + ABS_COORD_SIZE

''' The Constant GRID_SIZE. '''
GRID_SIZE = RECTANGLE_SIZE + 2 * DIMENSION_SIZE

''' The Constant LARGE_GRID_SIZE. '''
LARGE_GRID_SIZE = LARGE_RECTANGLE_SIZE + 2 * DIMENSION_SIZE

''' The Constant MIN_BYTES_POLYGON. '''
MIN_BYTES_POLYGON = HEADER_SIZE + ABS_COORD_SIZE + 2 * RELATIVE_COORD_SIZE

''' The Constant POINT_OFFSET_SIZE. '''
POINT_OFFSET_SIZE = 1

''' The Constant POINT_WITH_ACCESS_SIZE. '''
POINT_WITH_ACCESS_SIZE = HEADER_SIZE + FIRST_LRP_SIZE + LAST_LRP_SIZE + RELATIVE_COORD_SIZE

''' The Constant POINT_LOCATION_VERSION. '''
POINT_LOCATION_VERSION = 3

''' Base size for circle location '''
CIRCLE_BASE_SIZE = HEADER_SIZE + ABS_COORD_SIZE

LocationType = enum(
    # Location is UNKNOWN.
    'UNKNOWN',

    # line location.
    'LINE_LOCATION',

    # simple geo coordinates
    'GEO_COORDINATES',

    # point along a line
    'POINT_ALONG_LINE',

    # point of interest with an access point along a line
    'POI_WITH_ACCESS_POINT',

    # circle area location
    'CIRCLE',

    # polygon area location
    'POLYGON',

    # closed line area location
    'CLOSED_LINE',

    # rectangular area location
    'RECTANGLE',

    # grid area location
    'GRID'
    )


''' The Constant POINT_LOCATION_TYPES. '''
POINT_LOCATION_TYPES = {LocationType.GEO_COORDINATES, LocationType.POI_WITH_ACCESS_POINT, LocationType.POINT_ALONG_LINE}

''' The Constant AREA_LOCATION_VERSION. '''
AREA_LOCATION_VERSION = 3

''' The Constant AREA_LOCATION_TYPES. '''
AREA_LOCATION_TYPES = {LocationType.CIRCLE, LocationType.GRID, LocationType.CLOSED_LINE, LocationType.RECTANGLE, LocationType.POLYGON}

''' Side constants '''
ON_ROAD_OR_UNKNOWN = 0
RIGTH_SIDE = 1
LEFT_SIDE = 2
BOTH_SIDE = RIGTH_SIDE | LEFT_SIDE

''' Point has no sense of orientation, or determination of
    orientation is not applicable
'''
NO_ORIENTATION_OR_UNKNOWN = 0

''' Point has orientation from first LRP towards second LRP '''
WITH_LINE_DIRECTION = 1

''' Point has orientation from second LRP towards first LRP '''
AGAINST_LINE_DIRECTION = 2

''' Point has orientation in both directions '''
BOTH_DIRECTIONS = WITH_LINE_DIRECTION | AGAINST_LINE_DIRECTION
