# -*- coding: utf-8 -*-
''' Define functions for transforming encoded values

    .. moduleauthor:: David Marteau <david.marteau@mappy.com>

'''

from .utils import signum
from .constants import (BIT24FACTOR_REVERSED,
                        DECA_MICRO_DEG_FACTOR,
                        BEARING_SECTOR,
                        LENGTH_INTERVAL,
                        RELATIVE_OFFSET_LENGTH)


def _get32BitRepresentation(v):
    """ Calculate the 32 bit double value representation of a coordinate
        out of a 24 bit integer value representation.
        
        :param int v: Coordinate expressed in 24 bit integer value
        :return: Coordinate (in degrees)
        :rtype: float  
    """
    return (v - signum(v)*0.5) * BIT24FACTOR_REVERSED


def coordinates_values(lon, lat):
    """ Calculate the 32 bit double value representations of a pair of coordinates
        out of 24 bit integer values representation.
        
        :param int lon: Longitude expressed in 24 bit integer value
        :param int lat: Latitude expressed in 24 bit integer value
        :return: Pair of coordinates (in degrees)
        :rtype: float  
    """
    return (_get32BitRepresentation(lon),
            _get32BitRepresentation(lat))


def rel_coordinates_values(prev, blon, blat ):
    """ Calculate absolute corrdinates from relative coordinates to
        apply to the absolute coordinates of a reference position.
        
        :param Coords prev: Absolute coordinates of the reference geo point
        :param int blon: relative longitude expressed in decamicrodegrees
        :param int blat: relative latitude expressed in decamicrodegrees
        :return: Pair of coordinates (in degrees)
        :rtype: float
    """
    lon = (prev.lon + blon / DECA_MICRO_DEG_FACTOR)
    lat = (prev.lat + blat / DECA_MICRO_DEG_FACTOR)
    return lon, lat


def bearing_estimate(interval):
    """ Calculates an estimate for the bearing value. The bearing information
        provided by the location reference point indicates an interval in which
        the concrete value is. The approximation is the middle of that interval.
        
        :param int interval: bearing interval
        :return: bearing estimation (in degrees)
        :rtype: float
        
    """
    lower = interval * BEARING_SECTOR
    upper = (interval + 1) * BEARING_SECTOR
    return ((upper + lower) / 2)


def distance_estimate(interval):
    """ Calculates an estimate for a distance value. The distance information
        provided by the location reference point indicates an interval in which
        the concrete value is. The approximation is the middle of that interval.

        :param int interval: distance interval
        :return: distance estimation (in meters)
        :rtype: int
    """
    lower = interval * LENGTH_INTERVAL
    upper = (interval + 1) * LENGTH_INTERVAL
    return round(((upper + lower) / 2))


def relative_distance(offset):
    """ Calculates an estimate for a relative offset value. The offset information
        provided by the location reference point indicates an interval in which
        the concrete value (percentage) is. The approximation is the middle of
        that interval.

        :param int offset: offset interval
        :return: offset estimation (in %)
        :rtype: float
    """
    lower = offset * RELATIVE_OFFSET_LENGTH
    upper = (offset + 1) * RELATIVE_OFFSET_LENGTH
    return (lower + upper) / 2
