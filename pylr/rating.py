# -*- coding: utf-8 -*-
''' Handle Form Of Way (fow) rating

    .. moduleauthor:: David Marteau <david.marteau@mappy.com>

'''


from __future__ import absolute_import
from . import fow

"""
Indicates an excellent match of the attributes of the line with the
attributes specified in the LRP
"""
EXCELLENT = 3

"""
Indicates a good match of the attributes of the line with the
attributes specified in the LRP
"""
GOOD = 2

"""
Indicates an average match of the attributes of the line with the
attributes specified in the LRP
"""
AVERAGE = 1

"""
Indicates a poor match of the attributes of the line with the
attributes specified in the LRP
"""
POOR = 0


_to_index = lambda a, b: a + 8*b

_FOWRating = 64 * [0]
_FOWRating[_to_index(fow.UNDEFINED, fow.UNDEFINED)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.MOTORWAY)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.MULTIPLE_CARRIAGEWAY)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.SINGLE_CARRIAGEWAY)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.ROUNDABOUT)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.TRAFFICSQUARE)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.SLIPROAD)] = AVERAGE
_FOWRating[_to_index(fow.UNDEFINED, fow.OTHER)] = AVERAGE

_FOWRating[_to_index(fow.MOTORWAY, fow.MOTORWAY)] = EXCELLENT
_FOWRating[_to_index(fow.MOTORWAY, fow.MULTIPLE_CARRIAGEWAY)] = GOOD
_FOWRating[_to_index(fow.MOTORWAY, fow.SINGLE_CARRIAGEWAY)] = POOR
_FOWRating[_to_index(fow.MOTORWAY, fow.ROUNDABOUT)] = POOR
_FOWRating[_to_index(fow.MOTORWAY, fow.TRAFFICSQUARE)] = POOR
_FOWRating[_to_index(fow.MOTORWAY, fow.SLIPROAD)] = POOR
_FOWRating[_to_index(fow.MOTORWAY, fow.OTHER)] = POOR

_FOWRating[_to_index(fow.MULTIPLE_CARRIAGEWAY, fow.MULTIPLE_CARRIAGEWAY)] = EXCELLENT
_FOWRating[_to_index(fow.MULTIPLE_CARRIAGEWAY, fow.SINGLE_CARRIAGEWAY)] = GOOD
_FOWRating[_to_index(fow.MULTIPLE_CARRIAGEWAY, fow.ROUNDABOUT)] = AVERAGE
_FOWRating[_to_index(fow.MULTIPLE_CARRIAGEWAY, fow.TRAFFICSQUARE)] = POOR
_FOWRating[_to_index(fow.MULTIPLE_CARRIAGEWAY, fow.SLIPROAD)] = POOR
_FOWRating[_to_index(fow.MULTIPLE_CARRIAGEWAY, fow.OTHER)] = POOR

_FOWRating[_to_index(fow.SINGLE_CARRIAGEWAY, fow.SINGLE_CARRIAGEWAY)] = EXCELLENT
_FOWRating[_to_index(fow.SINGLE_CARRIAGEWAY, fow.ROUNDABOUT)] = AVERAGE
_FOWRating[_to_index(fow.SINGLE_CARRIAGEWAY, fow.TRAFFICSQUARE)] = AVERAGE
_FOWRating[_to_index(fow.SINGLE_CARRIAGEWAY, fow.SLIPROAD)] = POOR
_FOWRating[_to_index(fow.SINGLE_CARRIAGEWAY, fow.OTHER)] = POOR

_FOWRating[_to_index(fow.ROUNDABOUT, fow.ROUNDABOUT)] = EXCELLENT
_FOWRating[_to_index(fow.ROUNDABOUT, fow.TRAFFICSQUARE)] = AVERAGE
_FOWRating[_to_index(fow.ROUNDABOUT, fow.SLIPROAD)] = POOR
_FOWRating[_to_index(fow.ROUNDABOUT, fow.OTHER)] = POOR

_FOWRating[_to_index(fow.TRAFFICSQUARE, fow.TRAFFICSQUARE)] = EXCELLENT
_FOWRating[_to_index(fow.TRAFFICSQUARE, fow.SLIPROAD)] = POOR
_FOWRating[_to_index(fow.TRAFFICSQUARE, fow.OTHER)] = POOR

_FOWRating[_to_index(fow.SLIPROAD, fow.SLIPROAD)] = EXCELLENT
_FOWRating[_to_index(fow.SLIPROAD, fow.OTHER)] = POOR

_FOWRating[_to_index(fow.OTHER, fow.OTHER)] = EXCELLENT


def get_fow_rating_category(fow1, fow2):
    """ Get FOW rating category
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Polygon location
        :rtype: PolygonLocation
    """
    if fow1 > fow2:
        fow2, fow1 = fow1, fow2
    return _FOWRating[_to_index(fow1, fow2)]
