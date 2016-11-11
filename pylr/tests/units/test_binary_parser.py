# -*- coding: utf-8 -*-
"""
.. moduleauthor:: David Marteau <david.marteau@mappy.com>

Test the parsing of locations references coded in OpenLR.
"""


from __future__ import print_function
from __future__ import absolute_import
import sys

try:
    from unittest import TestCase
    from pylr import init_binary_parsing, parse_binary
    from pylr.tests.data import LOCATIONS
except:
    import traceback
    traceback.print_exc()
    raise


class TestOpenLRBinary(TestCase):

    def compare_coords(self, first, second, msg="Mismatching coordinates"):
        """Compare coordinates values with precision of 5 decimal places. 
        
        :param Coords first: First coordinates couple
        :param Coords second: Second coordinates couple
        :raises failureException: If coordinates values differ of more than 5 decimal places (for at least one component)
        """
        
        if round(abs(first.x-second.x), 5) != 0:
            raise self.failureException(msg)
        if round(abs(first.y-second.y), 5) != 0:
            raise self.failureException(msg)
    
    def compare_location_reference_point(self, first, second, msg="Mismatching location reference point"):
#         Coords(lon=2.371405363071578, lat=51.03174090361103), bear=21, orient=0, frc=3, fow=3, lfrcnp=3, dnp=29.), llrp=LocationReferencePoint(coords=Coords(lon=2.3711053630715777, lat=51.03164090361103), bear=5, orient=0, frc=3, fow=3, lfrcnp=None, dnp=None)
        self.assertEqual(first.coords, second.coords)
        self.assertEqual(first.bear, second.bear, "Mismatching bearing")
        self.assertEqual(first.orient, second.orient, "Mismatching orientation")
        self.assertEqual(first.frc, second.frc, "Mismatching functionnal road category")
        self.assertEqual(first.fow, second.fow, "Mismatching form of way")
        self.assertEqual(first.lfrcnp, second.lfrcnp, "Mismatching form of way")
    
    
    def compare_line_location(self, first, second, msg="Mismatching line location"):
        LineLocation(version=3,
                     type=LocationType.LINE_LOCATION,
                     flrp=LocationReferencePoint(coords=Coords(lon=2.371405363071578, lat=51.03174090361103),
                                                 bear=21,
                                                 orient=0,
                                                 frc=3,
                                                 fow=3,
                                                 lfrcnp=3,
                                                 dnp=29.),
                     llrp=LocationReferencePoint(coords=Coords(lon=2.3711053630715777, lat=51.03164090361103), bear=5, orient=0, frc=3, fow=3, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)

        self.assertEqual(first.version, second.version, "Mismatching version")
        self.assertEqual(first.type, second.type, "Mismatching type")
    
    
    def test_can_decode_header(self):
        """ OpenLR binary header parsing"""
        for d, v in LOCATIONS:
            p = init_binary_parsing(d, base64=True)

            self.assertEqual(p.version, 3, p.header)
            self.assertEqual(p.location_type, v.type, "{}\t{}\t{}".format(p.location_type, v.type, p.header))

    def test_can_decode_locations(self):
        """ OpenLR parse binary locations"""
        for d, v in LOCATIONS:
            p = parse_binary(d, base64=True)
            # print( "( '{}', {})".format(d, p), file=sys.stderr)
            self.assertEquals(p, v)
    
