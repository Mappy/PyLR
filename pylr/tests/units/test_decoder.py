# -*- coding: utf-8 -*-
'''
Created on 8 janv. 2014

.. moduleauthor:: David Marteau <david.marteau@mappy.com>

'''
from __future__ import print_function

from __future__ import absolute_import
try:
    from math import sqrt
    from collections import namedtuple
    from unittest import TestCase
    from pylr import (LineLocation,
                      CircleLocation,
                      PointAlongLineLocation,
                      LocationReferencePoint,
                      Coords,
                      Decoder,
                      DecoderError,
                      MapDatabase,
                      AGAINST_LINE_DIRECTION,
                      WITH_LINE_DIRECTION,
                      fow )
    from pylr.rating import get_fow_rating_category
    import pyproj
except:
    import traceback
    traceback.print_exc()
    raise

"""
LineLocation(version=3, type=1, flrp=LocationReferencePoint(coords=Coords(lon=2.371405363071578, lat=51.03174090361103), bear=21, orient=0, frc=3, fow=3, lfrcnp=3, dnp=29.), llrp=LocationReferencePoint(coords=Coords(lon=2.3711053630715777, lat=51.03164090361103), bear=5, orient=0, frc=3, fow=3, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
LineLocation(version=3, type=1, flrp=LocationReferencePoint(coords=Coords(lon=3.2568991184079317, lat=43.34901452043844), bear=21, orient=0, frc=4, fow=2, lfrcnp=4, dnp=322.0), llrp=LocationReferencePoint(coords=Coords(lon=3.253599118407932, lat=43.34799452043844), bear=7, orient=0, frc=4, fow=2, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
LineLocation(version=3, type=1, flrp=LocationReferencePoint(coords=Coords(lon=1.782649755469405, lat=49.28377747512205), bear=15, orient=0, frc=2, fow=3, lfrcnp=2, dnp=205.0), llrp=LocationReferencePoint(coords=Coords(lon=1.783229755469405, lat=49.28179747512205), bear=30, orient=0, frc=2, fow=3, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
LineLocation(version=3, type=1, flrp=LocationReferencePoint(coords=Coords(lon=-0.5087721347784577, lat=47.4383532998684), bear=22, orient=0, frc=2, fow=4, lfrcnp=2, dnp=440.0), llrp=LocationReferencePoint(coords=Coords(lon=-0.5144921347784577, lat=47.4371832998684), bear=6, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
( 'CwOyQCDbSxJPBwAA/osSXxM=', LineLocation(version=3, type=1, flrp=LocationReferencePoint(coords=Coords(lon=5.19789576527978, lat=46.20460152604006), bear=15, orient=0, frc=2, fow=2, lfrcnp=2, dnp=440.0), llrp=LocationReferencePoint(coords=Coords(lon=5.19789576527978, lat=46.20087152604006), bear=31, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), points=[], poffs=7.6171875, noffs=0)),
( 'CwB67CGukRxiCACyAbwaMXU=', LineLocation(version=3, type=1, flrp=LocationReferencePoint(coords=Coords(lon=0.675219297405838, lat=47.36516118027036), bear=2, orient=0, frc=3, fow=4, lfrcnp=3, dnp=498.0), llrp=LocationReferencePoint(coords=Coords(lon=0.676999297405838, lat=47.369601180270365), bear=17, orient=0, frc=3, fow=2, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=45.8984375)),
( 'K/6P+CKSvxJWCf0S/20SReM=', PointAlongLineLocation(version=3, type=3, flrp=LocationReferencePoint(coords=Coords(lon=-2.0216453075312537, lat=48.61858963943187), bear=22, orient=0, frc=2, fow=2, lfrcnp=2, dnp=557.0), llrp=LocationReferencePoint(coords=Coords(lon=-2.0291453075312536, lat=48.61711963943187), bear=5, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), poffs=88.8671875)),
( 'K/6P+SKSuBJGGAUn/1gSUyM=', PointAlongLineLocation(version=3, type=3, flrp=LocationReferencePoint(coords=Coords(lon=-2.0216238498591346, lat=48.61843943572703), bear=6, orient=0, frc=2, fow=2, lfrcnp=2, dnp=1436.0), llrp=LocationReferencePoint(coords=Coords(lon=-2.0084338498591348, lat=48.61675943572703), bear=19, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), poffs=13.8671875)),
( 'K//wgR8LkhNbAP/zAAgTS/8=', PointAlongLineLocation(version=3, type=3, flrp=LocationReferencePoint(coords=Coords(lon=-0.08511185646016545, lat=43.65729689577266), bear=27, orient=0, frc=2, fow=3, lfrcnp=2, dnp=29.0), llrp=LocationReferencePoint(coords=Coords(lon=-0.08524185646016545, lat=43.65737689577266), bear=11, orient=0, frc=2, fow=3, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'K//wRB8LkxNOAAAK/+sTXv8=', PointAlongLineLocation(version=3, type=3, flrp=LocationReferencePoint(coords=Coords(lon=-0.08642077445942678, lat=43.65731835344478), bear=14, orient=0, frc=2, fow=3, lfrcnp=2, dnp=29.0), llrp=LocationReferencePoint(coords=Coords(lon=-0.08632077445942678, lat=43.65710835344478), bear=30, orient=0, frc=2, fow=3, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'KwBVwSCh+RRXAf/i/9AUXP8=', PointAlongLineLocation(version=3, type=3, flrp=LocationReferencePoint(coords=Coords(lon=0.4710495471931884, lat=45.88973164536529), bear=23, orient=0, frc=2, fow=4, lfrcnp=2, dnp=88.0), llrp=LocationReferencePoint(coords=Coords(lon=0.4707495471931884, lat=45.889251645365285), bear=28, orient=0, frc=2, fow=4, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'KwBVzSCh7xRdAP/nABQUS/8=', PointAlongLineLocation(version=3, type=3, flrp=LocationReferencePoint(coords=Coords(lon=0.4713070392586169, lat=45.889517068644096), bear=29, orient=0, frc=2, fow=4, lfrcnp=2, dnp=29.0), llrp=LocationReferencePoint(coords=Coords(lon=0.4710570392586169, lat=45.889717068644096), bear=11, orient=0, frc=2, fow=4, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'CwSwrSIvJAo8+NUXIEMKPx3/uwXUCj7g218kAwo9Cv6RAfAKPQD/6wAdCj3B4usdywo9Lvf8B9gKPRL7XQI4CjoJ/UQAhgo4bvAuEN0KP48D3hvZCj4L/tACVgo+lOtlGdkKDQ==',
   LineLocation(version=3, type=1,
                flrp=LocationReferencePoint(coords=Coords(lon=6.595498323409102, lat=48.07144045806851), bear=28, orient=0, frc=1, fow=2, lfrcnp=1, dnp=14562.0),
                llrp=LocationReferencePoint(coords=Coords(lon=6.187078323409104, lat=48.55637045806851), bear=13, orient=0, frc=1, fow=2, lfrcnp=None, dnp=None),
                points=[
                        LocationReferencePoint(coords=Coords(lon=6.4856483234091025, lat=48.15403045806851), bear=31, orient=0, frc=1, fow=2, lfrcnp=1, dnp=1729.0),
                        LocationReferencePoint(coords=Coords(lon=6.484958323409103, lat=48.16895045806851), bear=30, orient=0, frc=1, fow=2, lfrcnp=1, dnp=13156.0),
                        LocationReferencePoint(coords=Coords(lon=6.391188323409103, lat=48.26114045806851), bear=29, orient=0, frc=1, fow=2, lfrcnp=1, dnp=615.0),
                        LocationReferencePoint(coords=Coords(lon=6.387518323409103, lat=48.26610045806851), bear=29, orient=0, frc=1, fow=2, lfrcnp=1, dnp=29.0),
                        LocationReferencePoint(coords=Coords(lon=6.387308323409103, lat=48.26639045806851), bear=29, orient=0, frc=1, fow=2, lfrcnp=1, dnp=11339.0),
                        LocationReferencePoint(coords=Coords(lon=6.312858323409103, lat=48.34266045806851), bear=29, orient=0, frc=1, fow=2, lfrcnp=1, dnp=2725.0),
                        LocationReferencePoint(coords=Coords(lon=6.292338323409103, lat=48.36274045806851), bear=29, orient=0, frc=1, fow=2, lfrcnp=1, dnp=1084.0),
                        LocationReferencePoint(coords=Coords(lon=6.280468323409103, lat=48.368420458068506), bear=26, orient=0, frc=1, fow=2, lfrcnp=1, dnp=557.0),
                        LocationReferencePoint(coords=Coords(lon=6.273468323409103, lat=48.369760458068505), bear=24, orient=0, frc=1, fow=2, lfrcnp=1, dnp=6475.0),
                        LocationReferencePoint(coords=Coords(lon=6.232968323409104, lat=48.41293045806851), bear=31, orient=0, frc=1, fow=2, lfrcnp=1, dnp=8409.0),
                        LocationReferencePoint(coords=Coords(lon=6.242868323409104, lat=48.484220458068506), bear=30, orient=0, frc=1, fow=2, lfrcnp=1, dnp=674.0),
                        LocationReferencePoint(coords=Coords(lon=6.239828323409103, lat=48.49020045806851), bear=30, orient=0, frc=1, fow=2, lfrcnp=1, dnp=8702.0)
                       ],
                poffs=0, noffs=0)),
)
"""

Node = namedtuple('Node', MapDatabase.Node._fields+('id', 'coords'))
Line = namedtuple('Line', MapDatabase.Line._fields+('start', 'end', 'bearin', 'bearout'))

gall_proj = pyproj.Proj("+init=esri:54016")

def distance(xy_1, xy_2):
    (x1, y1), (x2, y2) = xy_1, xy_2
    return sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))


# Define a fake database


class DummyDatabase(MapDatabase):

    _Nodes = (Node(id='flrp1', distance=0, coords=Coords(186664.62018550665, lat=5197088.916676804)),
              Node(id='llrp1', distance=0, coords=Coords(186641.00575546117, lat=5197077.25019193)),
              Node(id='flrp2', distance=0, coords=Coords(256366.05465574207, lat=4327314.792105144)),
              Node(id='llrp2', distance=0, coords=Coords(256106.2959252422, lat=4327202.566624085)),
              )

    _Lines = (Line(id='Line1', bear=21, frc=3, fow=3, projected_len=None, len=0,
                   start='flrp1', end='llrp1', bearin=4, bearout=21),
              Line(id='Line2', bear=5, frc=3, fow=3, projected_len=None, len=0,
                   start='llrp1', end='flrp1', bearin=21, bearout=4),
              Line(id='Line3', bear=5, frc=3, fow=3,
                   projected_len=None, len=0,
                   start='llrp1', end='flrp1', bearin=4, bearout=21),
              )

    def connected_lines(self, node, frc_max, beardir):
        if beardir == AGAINST_LINE_DIRECTION:
            # Search for inwards arcs
            lines = (l for l in self._Lines if l.end == node.id and frc_max >= l.frc)
        else:
            lines = (l for l in self._Lines if l.start == node.id and frc_max >= l.frc)

        for l in lines:
            if beardir == AGAINST_LINE_DIRECTION:
                # we need to replace bearing
                yield l._replace(bear=l.bearin)
            else:
                yield l._replace(bear=l.bearout)

    def find_closeby_nodes(self, coords, max_node_dist):
        coords = gall_proj(*coords)
        for n in self._Nodes:
            dist = distance(coords, n.coords)
            if dist <= max_node_dist:
                yield n._replace(distance=dist)

    def find_closeby_lines(self, coords, max_node_dist, frc_max, beardir):
        return ()

    def calculate_route(self, l1, l2, maxdist, lfrc, islastrp):
        pass


LRP1 = LocationReferencePoint(coords=Coords(lon=2.371405363071578, lat=51.03174090361103),
                              bear=21, orient=0, frc=3, fow=3, lfrcnp=3, dnp=29.)

LRP2 = LocationReferencePoint(coords=Coords(lon=2.3711053630715777, lat=51.03164090361103),
                              bear=5, orient=0, frc=3, fow=3, lfrcnp=None, dnp=None)

LOCATION1 = LineLocation(version=3, type=1, flrp=LRP1, llrp=LRP2, points=[], poffs=0, noffs=0)


class TestDecoder(TestCase):

    @classmethod
    def setUpClass(cls):
        TestDecoder._database = DummyDatabase()

    def setUp(self):
        self.decoder = Decoder(TestDecoder._database)

    def test_10_rating(self):
        """ OpenLR decoder: check acceptance rating """
        lrp = LRP1
        line = self._database._Lines[0]
        rating = self.decoder.rating(lrp, line, 0)

        self.assertGreaterEqual(rating, self.decoder._min_acc_rating)

    def test_11_rating(self):
        """ OpenLR decoder: check rating with invalid bearing"""
        lrp = LRP2
        line = self._database._Lines[0]
        rating = self.decoder.rating(lrp, line, 0)

        # Bearing is not acceptable
        self.assertEqual(rating, -1)

    def test_20_find_candidate_nodes(self):
        """ OpenLR decoder: find candidate nodes """
        lrp = LRP1
        nodes = sorted(list(self.decoder.find_candidate_nodes(lrp)), key=lambda n: n.distance)

        self.assertGreaterEqual(len(nodes), 1)
        self.assertEquals(nodes[0].id, 'flrp1')

#         lines = list(self._database.connected_lines(nodes[0], frc_max=5, beardir=WITH_LINE_DIRECTION))
#         self.assertGreaterEqual(len(lines), 1)
#         self.assertEquals(lines[0].id, 'Line1')

    def test_21_find_candidate_lines(self):
        """ OpenLR decoder: find candidate lines """
        lrp = LRP1
        lines = self.decoder.find_candidate_lines(lrp)
        self.assertGreaterEqual(len(lines), 1)
        self.assertEquals(lines[0][0].id, 'Line1', lines)
        
    def test_fow_rating(self):
        """ OpenLR decoder: test fow rating symmetry """
        fows = [fow.UNDEFINED,
                fow.MOTORWAY,
                fow.MULTIPLE_CARRIAGEWAY,
                fow.SINGLE_CARRIAGEWAY,
                fow.ROUNDABOUT,
                fow.TRAFFICSQUARE,
                fow.SLIPROAD,
                fow.OTHER]

        for fow1 in fows:
            for fow2 in fows:
                self.assertEquals(get_fow_rating_category(fow1,fow2),
                                  get_fow_rating_category(fow2,fow1))
