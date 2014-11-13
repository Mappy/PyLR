# -*- coding: utf-8 -*-
'''
Created on 4 déc. 2013

.. moduleauthor:: David Marteau <david.marteau@mappy.com>

OpenLR decoder

'''

from ._parser import (BinaryParseError,
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

from ._binary import (Coords,
                      LocationReferencePoint)

from ._constants import (LocationType,
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



import _fow as fow


from ._decoder import (DecoderError,
                       DecoderInvalidLocation,
                       RouteSearchException,
                       RouteNotFoundException,
                       RouteConstructionFailed,
                       MapDatabase,
                       DecoderBase,
                       RatingCalculator,
                       ClassicDecoder)

Decoder = ClassicDecoder
