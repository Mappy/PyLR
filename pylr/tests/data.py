# -*- coding: utf-8 -*-
'''
Created on 6 déc. 2013

.. moduleauthor:: David Marteau <david.marteau@mappy.com>
'''

from __future__ import absolute_import
from pylr import  ( LocationType,
                    BBox,
                    LineLocation,
                    GeoCoordinateLocation,
                    CircleLocation,
                    RectangleLocation,
                    PolygonLocation,
                    PoiWithAccessPointLocation,
                    GridLocation,
                    PointAlongLineLocation,
                    ClosedLineLocation,
                    Coords,
                    LocationReferencePoint,
                    ON_ROAD_OR_UNKNOWN,
                    NO_ORIENTATION_OR_UNKNOWN)


'''
LineLocation( version=3, type=LocationType.POINT_ALONG_LINE, 
              flrp=LocationReferencePoint( Coords(lon=2.371405363071578 , lat=51.03174090361103), bear=21, orient=0, frc=3, fow=3, lfrcnp=3, dnp=29.0)  ),
              llrp=LocationReferencePoint( Coords(lon=2.3711053630715777, lat=51.03164090361103), bear=5 , orient=0, frc=3, fow=3, lfrcnp=None, dnp=None), 
              points=[], poffs=0, noffs=0)
              
PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, 
              flrp=LocationReferencePoint( Coords(lon=-2.0216238498591346, lat=48.61843943572703), bear=6, orient=0, frc=2, fow=2, lfrcnp=2, dnp=1436.0), 
              llrp=LocationReferencePoint( Coords(lon=-2.0084338498591348, lat=48.61675943572703), bear=19, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), 
              poffs=13.8671875)

'''           

LOCATIONS = (            
( 'CwGvtCRKDBt1AP/i//YbBQ==', LineLocation(version=3, type=LocationType.LINE_LOCATION, flrp=LocationReferencePoint(coords=Coords(lon=2.371405363071578, lat=51.03174090361103), bear=21, orient=0, frc=3, fow=3, lfrcnp=3, dnp=29.), llrp=LocationReferencePoint(coords=Coords(lon=2.3711053630715777, lat=51.03164090361103), bear=5, orient=0, frc=3, fow=3, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
( 'CwJQ5x7TcyKVBf62/5oiBw==', LineLocation(version=3, type=LocationType.LINE_LOCATION, flrp=LocationReferencePoint(coords=Coords(lon=3.2568991184079317, lat=43.34901452043844), bear=21, orient=0, frc=4, fow=2, lfrcnp=4, dnp=322.0), llrp=LocationReferencePoint(coords=Coords(lon=3.253599118407932, lat=43.34799452043844), bear=7, orient=0, frc=4, fow=2, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
( 'CwFEhiML1xNPAwA6/zoTHg==', LineLocation(version=3, type=LocationType.LINE_LOCATION, flrp=LocationReferencePoint(coords=Coords(lon=1.782649755469405, lat=49.28377747512205), bear=15, orient=0, frc=2, fow=3, lfrcnp=2, dnp=205.0), llrp=LocationReferencePoint(coords=Coords(lon=1.783229755469405, lat=49.28179747512205), bear=30, orient=0, frc=2, fow=3, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
( 'C/+jYSG75BRWB/3E/4sSBg==', LineLocation(version=3, type=LocationType.LINE_LOCATION, flrp=LocationReferencePoint(coords=Coords(lon=-0.5087721347784577, lat=47.4383532998684), bear=22, orient=0, frc=2, fow=4, lfrcnp=2, dnp=440.0), llrp=LocationReferencePoint(coords=Coords(lon=-0.5144921347784577, lat=47.4371832998684), bear=6, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=0)),
( 'CwOyQCDbSxJPBwAA/osSXxM=', LineLocation(version=3, type=LocationType.LINE_LOCATION, flrp=LocationReferencePoint(coords=Coords(lon=5.19789576527978, lat=46.20460152604006), bear=15, orient=0, frc=2, fow=2, lfrcnp=2, dnp=440.0), llrp=LocationReferencePoint(coords=Coords(lon=5.19789576527978, lat=46.20087152604006), bear=31, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), points=[], poffs=7.6171875, noffs=0)),
( 'CwB67CGukRxiCACyAbwaMXU=', LineLocation(version=3, type=LocationType.LINE_LOCATION, flrp=LocationReferencePoint(coords=Coords(lon=0.675219297405838, lat=47.36516118027036), bear=2, orient=0, frc=3, fow=4, lfrcnp=3, dnp=498.0), llrp=LocationReferencePoint(coords=Coords(lon=0.676999297405838, lat=47.369601180270365), bear=17, orient=0, frc=3, fow=2, lfrcnp=None, dnp=None), points=[], poffs=0, noffs=45.8984375)),
( 'CwSwrSIvJAo8+NUXIEMKPx3/uwXUCj7g218kAwo9Cv6RAfAKPQD/6wAdCj3B4usdywo9Lvf8B9gKPRL7XQI4CjoJ/UQAhgo4bvAuEN0KP48D3hvZCj4L/tACVgo+lOtlGdkKDQ==', 
   LineLocation(version=3, type=LocationType.LINE_LOCATION, 
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
( 'IwOgDCUOIg==', GeoCoordinateLocation(version=3, type=LocationType.GEO_COORDINATES, coords=Coords(lon=5.097903013205062, lat=52.108873128642514))),
( 'K/6P+CKSvxJWCf0S/20SReM=', PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, flrp=LocationReferencePoint(coords=Coords(lon=-2.0216453075312537, lat=48.61858963943187), bear=22, orient=0, frc=2, fow=2, lfrcnp=2, dnp=557.0), llrp=LocationReferencePoint(coords=Coords(lon=-2.0291453075312536, lat=48.61711963943187), bear=5, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), poffs=88.8671875)),
( 'K/6P+SKSuBJGGAUn/1gSUyM=', PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, flrp=LocationReferencePoint(coords=Coords(lon=-2.0216238498591346, lat=48.61843943572703), bear=6, orient=0, frc=2, fow=2, lfrcnp=2, dnp=1436.0), llrp=LocationReferencePoint(coords=Coords(lon=-2.0084338498591348, lat=48.61675943572703), bear=19, orient=0, frc=2, fow=2, lfrcnp=None, dnp=None), poffs=13.8671875)),
( 'K//wgR8LkhNbAP/zAAgTS/8=', PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, flrp=LocationReferencePoint(coords=Coords(lon=-0.08511185646016545, lat=43.65729689577266), bear=27, orient=0, frc=2, fow=3, lfrcnp=2, dnp=29.0), llrp=LocationReferencePoint(coords=Coords(lon=-0.08524185646016545, lat=43.65737689577266), bear=11, orient=0, frc=2, fow=3, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'K//wRB8LkxNOAAAK/+sTXv8=', PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, flrp=LocationReferencePoint(coords=Coords(lon=-0.08642077445942678, lat=43.65731835344478), bear=14, orient=0, frc=2, fow=3, lfrcnp=2, dnp=29.0), llrp=LocationReferencePoint(coords=Coords(lon=-0.08632077445942678, lat=43.65710835344478), bear=30, orient=0, frc=2, fow=3, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'KwBVwSCh+RRXAf/i/9AUXP8=', PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, flrp=LocationReferencePoint(coords=Coords(lon=0.4710495471931884, lat=45.88973164536529), bear=23, orient=0, frc=2, fow=4, lfrcnp=2, dnp=88.0), llrp=LocationReferencePoint(coords=Coords(lon=0.4707495471931884, lat=45.889251645365285), bear=28, orient=0, frc=2, fow=4, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'KwBVzSCh7xRdAP/nABQUS/8=', PointAlongLineLocation(version=3, type=LocationType.POINT_ALONG_LINE, flrp=LocationReferencePoint(coords=Coords(lon=0.4713070392586169, lat=45.889517068644096), bear=29, orient=0, frc=2, fow=4, lfrcnp=2, dnp=29.0), llrp=LocationReferencePoint(coords=Coords(lon=0.4710570392586169, lat=45.889717068644096), bear=11, orient=0, frc=2, fow=4, lfrcnp=None, dnp=None), poffs=99.8046875)),
( 'KwOg5iUNnCOTAv+D/5QjQ1j/gP/r', PoiWithAccessPointLocation(version=3,
                                                         type=LocationType.POI_WITH_ACCESS_POINT,
                                                         flrp=LocationReferencePoint(coords=Coords(lon=5.102580785727012, lat=52.105997800578564), bear=19, orient=0, frc=4, fow=3, lfrcnp=4, dnp=147.0),
                                                         llrp=LocationReferencePoint(coords=Coords(lon=5.101330785727012, lat=52.10491780057856),   bear=3,   orient=0, frc=4, fow=3, lfrcnp=None, dnp=None),
                                                         poffs=34.5703125,
                                                         coords=Coords(lon=5.101300785727012, lat=52.10578780057856))
                                                         ),
( 'AwOgxCUNmwEs', CircleLocation(version=3, type=LocationType.CIRCLE, coords=Coords(lon=5.101851224874965, lat=52.105976342906445), radius=300)),
( 'EwOgUCUNEwJFAH//yAEv/vIAx/7F/z0=', PolygonLocation(version=3, type=LocationType.POLYGON,
                                                      points=[
                                                                Coords(lon=5.099362134909156, lat=52.103058099498256),
                                                                Coords(lon=5.105172134909156, lat=52.104328099498254),
                                                                Coords(lon=5.104612134909156,  lat=52.107358099498256),
                                                                Coords(lon=5.101912134909156, lat=52.109348099498256),
                                                                Coords(lon=5.0987621349091565, lat=52.107398099498255)
                                                             ]
                                                      )
                                                      ),
( 'WwOgrCUNaiOLBiMD', 
   ClosedLineLocation(version=3, type=LocationType.CLOSED_LINE, 
                flrp=LocationReferencePoint(coords=Coords(lon=5.101336240744107, lat=52.104924916972614), bear=11, orient=0, frc=4, fow=3, lfrcnp=4, dnp=381), 
                points=[], frc=4, fow=3, bear=3)),
)
( 'QwOgcSUNGgGIAX8=', RectangleLocation(version=3, type=LocationType.RECTANGLE, bbox=BBox(minx=5.100070238089084, miny=52.10320830320309, maxx=5.103990238089084, maxy=52.10703830320309))),
( 'QwOgNiUM5wFVANsAAwAC', GridLocation(version=3, type=LocationType.GRID, bbox=BBox(5.098804235434061,52.10211396192502,5.102214235434061,52.10430396192502), cols=3, rows=2)),
