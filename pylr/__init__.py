# -*- coding: utf-8 -*-
'''
Created on 4 déc. 2013

.. moduleauthor:: Mappy S.A

OpenLR decoder

'''

__version_info__=(0,1,0)
__version__ = "{0}.{1}.{2}".format(*__version_info__)


from .parser import (BinaryParseError,
                     BinaryVersionError,
                     InvalidDataSizeError,
                     init_binary_parsing,
                     parse_binary,
                     LocationType,
                     LineLocation,
                     GeoCoordinateLocation,
                     BBox,
                     CircleLocation,
                     RectangleLocation,
                     GridLocation,
                     PolygonLocation,
                     PoiWithAccessPointLocation,
                     ClosedLineLocation,
                     PointAlongLineLocation,
                     GeoCoordinateLocation,
                     PoiWithAccessPointLocation,
                     RectangleLocation,
                     BBox)

from .binary import (Coords,
                     LocationReferencePoint)

from .constants import (LocationType,
                        LENGTH_INTERVAL,
                        BEARING_SECTOR,
                        RELATIVE_OFFSET_LENGTH,
                        RIGTH_SIDE,
                        LEFT_SIDE,
                        BOTH_SIDE,
                        NO_ORIENTATION_OR_UNKNOWN,
                        WITH_LINE_DIRECTION,
                        AGAINST_LINE_DIRECTION,
                        BOTH_DIRECTIONS,
                        ON_ROAD_OR_UNKNOWN)



import fow


from .decoder import (DecoderError,
                      DecoderInvalidLocation,
                      RouteSearchException,
                      RouteNotFoundException,
                      RouteConstructionFailed,
                      MapDatabase,
                      DecoderBase,
                      RatingCalculator,
                      ClassicDecoder)

Decoder = ClassicDecoder
