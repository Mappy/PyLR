# -*- coding: utf-8 -*-
''' Support definition and intermediate parsing of binary encoded locations

.. moduleauthor:: David Marteau <david.marteau@mappy.com>

'''

from collections import namedtuple
from .values import (coordinates_values,
                     rel_coordinates_values,
                     distance_estimate,
                     relative_distance)

from .constants import (BINARY_VERSION_2, BINARY_VERSION_3)

# lon (float) : longitude (in degrees)
# lat (float) : latituded (in degrees)
Coords = namedtuple('Coords',  ('lon', 'lat'))
"""Coordinates, expressed as a pair of float values (in degrees)."""

# coords (Coords) : Coordinates
# bear : bearing ; expressed as a sector number describing a bearing range
# orient : orientation, expressed as a bit field
# frc : functionnal road class, expressed as a bit field
# fow : form of way, expressed as a bit field
# lfrcnp : lowest FRC to next point, expressed as a bit field
# dnp : distance to next LR-point, expressed in meters
LocationReferencePoint = namedtuple('LocationReferencePoint',  (
    'coords', 'bear', 'orient', 'frc', 'fow',  'lfrcnp', 'dnp'))
"Location Reference Point. Used to define several kinds of lcoation (lines, ...)"

RADIUS_BITS = ('uint:8', 'uint:16', 'uint:24', 'uint:32')
""" Number of bits needed to code the radius for a circle location reference.
"""

# Bit fields used to read physical data
RFU_BITS = 'uint:1'
SIDE_OR_ORIENTATION_BITS = 'uint:2' 
FRC_BITS = 'uint:3'
FOW_BITS = 'uint:3'
LFRCNP_BITS = 'uint:3'
BEAR_BITS = 'uint:5'
DNP_BITS = 'uint:8'
POFFF_BITS = 'uint:1'
NOFFF_BITS = 'uint:1'
NR_RFU2 = 'uint:2'
NR_RFU3 = 'uint:3'
GRID_CELL_BITS = 'uint:16'
ABS_COORDS_BITS = 'int:24'
RLRP_COORDS_BITS = 'int:16'
OFFSET_BITS = 'uint:8'

# Caution : the attribute names refer to the reference implementation,
# not to the specifications
ATTR1_BITS = (SIDE_OR_ORIENTATION_BITS, FRC_BITS, FOW_BITS)
ATTR2_BITS = (LFRCNP_BITS, BEAR_BITS)
ATTR3_BITS = (DNP_BITS,)
ATTR4_BITS = (RFU_BITS, POFFF_BITS, NOFFF_BITS, BEAR_BITS)
ATTR5_BITS = (NR_RFU2, FRC_BITS, FOW_BITS)
ATTR6_BITS = (NR_RFU3, BEAR_BITS)

def _parse_attr1(rb):
    ''' Parse the raw binary data bits defined by ATTR1_BITS
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: orientation, FRC, FOW
        :rtype: int, int, int
    '''
    orient, frc, fow = rb.getbits(*ATTR1_BITS)
    return orient, frc, fow


def _parse_attr2(rb):
    ''' Parse the raw binary data bits defined by ATTR2_BITS
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: lowest FRC to next LR-point, bearing
        :rtype: int, int
    '''
    lfrcnp, bear = rb.getbits(*ATTR2_BITS)
    return lfrcnp, bear


def _parse_attr3(rb):
    ''' Parse the raw binary data bits defined by ATTR3_BITS
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: distance interval to next LR-point
        :rtype: int
    '''
    dnp = rb.getbits(*ATTR3_BITS)
    return dnp


def _parse_attr4(rb):
    ''' Parse the raw binary data bits defined by ATTR3_BITS
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: positive offset length interval, negative offset length interval, bearing sector
        :rtype: int, int, int
    '''
    _, pofff, nofff, bear = rb.getbits(*ATTR4_BITS)
    return pofff, nofff, bear


def _parse_attr5(rb):
    ''' Parse the raw binary data bits defined by ATTR3_BITS
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Functionnal Road Class, Form Of Way
        :rtype: int, int
    '''
    _, frc, fow = rb.getbits(*ATTR5_BITS)
    return frc, fow


def _parse_attr6(rb):
    ''' Parse the raw binary data bits defined by ATTR3_BITS
        :param _RawBinaryData rb: Binary data describing the location
        :returns: bearing sector
        :rtype: int
    '''
    _, bear = rb.getbits(*ATTR6_BITS)
    return bear


def _parse_coordinates(rb, bits, rel):
    ''' Parse the raw binary data bits to read coordinates. These ones can be read as absolute or relative coordinates.
        In the last case, the third parameter must be provided. Else, its value must be None.
        
        :param _RawBinaryData rb: Binary data describing the location
        :param string bits: String describing the number of bits to read ; may be RLRP_COORDS_BITS or ABS_COORDS_BITS.
        :param Coords rel: If the ccordinates to read are supposed to be relative, this parameter gives the reference coordinates.
                           Its value is ignored when asbulute coordinates is set for the second parameter.
        :returns: Coordinates
        :rtype: Coords
    '''
    lon, lat = rb.getbits(bits, bits)
    if rel:
        lon, lat = rel_coordinates_values(rel, lon, lat)
    else:
        lon, lat = coordinates_values(lon, lat)
    return Coords(lon, lat)

def _parse_relative_coordinates(rb, rel):
    ''' Parse the raw binary data bits to read relative coordinates.
    
        :param _RawBinaryData rb: Binary data describing the location
        :param Coords rel: Reference coordinates
        :returns: Coordinates
        :rtype: Coords
    '''
    return _parse_coordinates(rb, RLRP_COORDS_BITS, rel)


def _parse_absolute_coordinates(rb):
    ''' Parse the raw binary data bits to read absolute coordinates.
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Coordinates
        :rtype: Coords
    '''
    return _parse_coordinates(rb, ABS_COORDS_BITS, None)


def _parse_lrp(rb, bits, rel_coords):
    ''' Parse location reference point
    
        :param _RawBinaryData rb: Binary data describing the location
        :param string bits: String describing the number of bits to read ; may be RLRP_COORDS_BITS or ABS_COORDS_BITS.
        :param Coords rel_coords: Reference coordinates.
        :returns: Location Reference Point
        :rtype: LocationReferencePoint
    '''
    coords = _parse_coordinates(rb, bits, rel_coords)
    orient, frc, fow = _parse_attr1(rb)
    frcnp, bear = _parse_attr2(rb)
    dnp, = _parse_attr3(rb)

    dnp = distance_estimate(dnp)

    return LocationReferencePoint(coords, bear, orient, frc, fow, frcnp, dnp)


def _parse_first_lrp(rb):
    ''' Parse the first location reference point (coded in absolute coordinates) of a location reference
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Location Reference Point
        :rtype: LocationReferencePoint
    '''
    return _parse_lrp(rb, ABS_COORDS_BITS, None)


def _parse_intermediate_lrp(rb, rel):
    ''' Parse any intermediate location reference point (coded in relative coordinates) of a location reference
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Location Reference Point
        :rtype: LocationReferencePoint
    '''
    return _parse_lrp(rb, RLRP_COORDS_BITS, rel.coords)


def _parse_last_line_lrp(rb, rel, sided=False):
    ''' Parse the last location reference point for some kinds of location references
    
        :param _RawBinaryData rb: Binary data describing the location
        :param Coords rel: Reference coordinates
        :param bool sided: Must be set to True if a diding info must be read
        :returns: Location Reference Point, positive offset length interval, negative offset length interval
        :rtype: LocationReferencePoint, int, int
    '''
    coords = _parse_coordinates(rb, RLRP_COORDS_BITS, rel.coords)
    side, frc, fow = _parse_attr1(rb)
    pofff, nofff, bear = _parse_attr4(rb)

    return LocationReferencePoint(coords, bear, side, frc, fow, None, None), pofff, nofff


def _parse_last_closed_line_attrs(rb):
    ''' Parse the last location reference point's attributes for the closed line location reference
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Functionnal Road Class, Form Of Way, bearing sector
        :rtype: int, int, int
    '''
    frc, fow = _parse_attr5(rb)
    bear = _parse_attr6(rb)

    return frc, fow, bear


def _parse_offset(rb):
    ''' Parse positive or negative offset for some kinds of location references
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Estimate distance, in meters
        :rtype: int
    '''
    offs, = rb.getbits(OFFSET_BITS)
    if rb.version == BINARY_VERSION_2:
        offs = distance_estimate(offs)
    elif rb.version == BINARY_VERSION_3:
        offs = relative_distance(offs)
    return offs


def _parse_radius(rb, radius_size):
    ''' Parse radius of circle location references.
    
        :param _RawBinaryData rb: Binary data describing the location
        :param int radius_size: Number of bytes needed to read the radius
        :returns: Radius, in meters
        :rtype: int
    '''
    radius, = rb.getbits(RADIUS_BITS[radius_size-1])
    return radius


def _parse_grid_dimensions(rb):
    ''' Parse grid location reference dimensions
    
        :param _RawBinaryData rb: Binary data describing the location
        :returns: Number of columns, number of rows
        :rtype: int, int
    '''
    cols, = rb.getbits(GRID_CELL_BITS)
    rows, = rb.getbits(GRID_CELL_BITS)
    return cols, rows
