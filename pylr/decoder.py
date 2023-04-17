# -*- coding: utf-8 -*-
''' OpenLR decoder and database interfaces

    .. moduleauthor:: David Marteau <david.marteau@mappy.com>

    Pylr use an abstract mapdatabase interface for accessing grapth data.
    The map database is passed to the decoder for calculating route and shortest path between
    location reference points.
'''
from __future__ import print_function, absolute_import
from collections import namedtuple
from itertools import groupby, chain
from pylr import rating as Rating
from .constants import (LocationType,
                        WITH_LINE_DIRECTION,
                        AGAINST_LINE_DIRECTION,
                        BINARY_VERSION_2,
                        BINARY_VERSION_3)


''' The Max_ node_ distance '''
MAX_NODE_DIST = 100

''''The node factor.'''
NODE_FACTOR = 3

'''The line factor'''
LINE_FACTOR = 3

'''The FRC variance'''
FRC_VARIANCE = 2

'''The minimum accepted rating'''
MIN_ACC_RATING = 800

'''Max number of retries'''
MAX_NR_RETRIES = 3

'''The same line degradation'''
SAME_LINE_DEGRAD = 0.10

'''Connected route increase'''
CONNECT_ROUTE_INC = 0.10

'''DNP variance'''
DNP_VARIANCE = 118

'''FRC rating'''
FRC_RATING = {Rating.EXCELLENT: 100,
              Rating.GOOD: 75,
              Rating.AVERAGE: 50,
              Rating.POOR: 0}

'''FRC_Intervals'''
FRC_INTERVALS = {Rating.EXCELLENT: 0,
                 Rating.GOOD: 1,
                 Rating.AVERAGE: 2}

'''FOW rating'''
FOW_RATING = {Rating.EXCELLENT: 100,
              Rating.GOOD: 50,
              Rating.AVERAGE: 50,
              Rating.POOR: 25}

'''Bearing rating'''
BEAR_RATING = {Rating.EXCELLENT: 100,
               Rating.GOOD: 50,
               Rating.AVERAGE: 25,
               Rating.POOR: 0}

# Compare bearing using integer bearing values

'''Bearing intervals'''
BEAR_INTERVALS = {Rating.EXCELLENT: 0,
                  Rating.GOOD: 1,
                  Rating.AVERAGE: 2}

'''Max bearing diff'''
MAX_BEAR_DIFF = 8  # 90deg

HALF_CIRCLE = 16  # 180deg

FULL_CIRCLE = 32  # 360deg

'''Calc affected lines'''
CALC_AFFECTED_LINES = False

'''Lines directly factor'''
LINES_DIRECTLY_FACTOR = 0.95

'''CompTime4Cache'''
COMP_TIME_4_CACHE = 0

# ----------------
# Special values
# ----------------

# Define empty route
EMPTY_ROUTE = ((), 0)

# ----------------
# Decoder exceptions
# ----------------


class DecoderError(Exception):
    pass


class DecoderInvalidLocation(DecoderError):
    pass


class DecoderNodesNotFound(DecoderError):
    pass


class DecoderNoCandidateLines(DecoderError):
    pass


class RouteSearchException(DecoderError):
    pass


class RouteNotFoundException(RouteSearchException):
    pass


class InvalidRouteLength(RouteNotFoundException):
    pass


class RouteConstructionFailed(RouteSearchException):
    pass

# ----------------
# Map database
# ----------------


class MapDatabase(object):
    """ Abstract interface used by the decoder object.

        Implementor of database should inherit from this abstract class.

        MapDatabase defines two data structure as named tuples:

        :py:class:`MapDatabase.Node`

        :py:class:`MapDatabase.Line`

        These structures may be extended by MapDatabase implementor accordings to their specific needs.
    """

    Node = namedtuple('Node', ('distance',))
    """
        .. attribute:: distance

           The distance from the search location
    """

    Line = namedtuple('Line', ('id', 'bear', 'frc', 'fow', 'len', 'projected_len'))
    """
        .. attribute:: id

            id of the line

        .. attribute:: bear

            the bearing according to the start node

        .. attribute:: frc

             the frc of the line

        .. attribute:: fow

            the fow of the line

        .. attribute:: projected_len

            return the value of the projected length of the search location
            (i.e) the distance between the start node and the projection of the
            point given by the search coordinates. None if the line is not
            projected
    """

    def connected_lines(self, node, frc_max, beardir):
        """ Return connected lines to/from the node 'node'

            :param frc_max: the frc max of the requested lines
            :param beardir: select the inwards (AGAINST_LINE_DIRECTION)
            or the outwards (WITH_LINE_DIRECTION) connected lines

            return an iterable of objects of type Line
        """
        raise NotImplementedError("MapDatabase:connectedlines")

    def find_closeby_nodes(self, coords, max_node_dist):
        """ Look for all nodes at less than max_node_dist from
            the given coordinates

            :param coords: an tuple or iterable holding location coordinates
            :param max_node_dist: max distance to nearch for nodes

            return an iterable of Node objects
        """
        raise NotImplementedError("MapDatabase:find_closeby_nodes")

    def find_closeby_lines(self, coords, max_node_dist, frc_max, beardir):
        """ Look for all lines at less than max_node_dist from
            the given coordinates

            :param coords: an tuple or iterable holding location coordinates
            :param max_node_dist: max distance to nearch for nodes
            :param frc_max: the frc max of the requested line
            :param beardir: select the inwards (AGAINST_LINE_DIRECTION)
            or the outwards (WITH_LINE_DIRECTION) connected lines

            return an iterable of Line objects
        """
        raise NotImplementedError("MapDatabase:find_closeby_lines")

    def calculate_route(self, l1, l2, maxdist, lfrc, islastrp):
        """ Calculate the shortest paths between two lines

            :param l1: the first candidate line to begin the search from
            :param l2: the second candidate line to stop the search to
            :param maxdist: The maximum distance allowed
            :param lfrc: The least frc allowed
            :param islastrp: True if we are calculating the route to the last
            reference point
            :return: (route, length) where route is an iterable holding the lines found
            and length the calculated length  of the route

            The method must throw a RouteNotFoundException or a RouteConstructionFailed
            exception in case a route cannot be calculated
        """
        raise NotImplementedError("MapDatabase:calculate_route")

# ----------------
# Decoder
# ----------------


class DecoderBase(object):
    pass


class RatingCalculator(object):
    """ Implement default rating calculation
    """

    RatingDetails = namedtuple('RatingDetails', ('bear_rating', 'frc_rating', 'fow_rating'))

    def _frc_rating(self, frc, linefrc):
        diff = abs(frc - linefrc)
        for cat in (Rating.EXCELLENT, Rating.GOOD, Rating.AVERAGE):
            if diff <= FRC_INTERVALS[cat]:
                return FRC_RATING[cat]
        return FRC_RATING[Rating.POOR]

    def _fow_rating(self, fow, linefow):
        return FOW_RATING[Rating.get_fow_rating_category(fow, linefow)]

    def _distance_rating(self, dist):
        return max(0, self._max_node_dist - round(dist))

    def _bear_rating(self, bearing, linebear):
        diff = abs(bearing - linebear)
        if diff > HALF_CIRCLE:
            diff = FULL_CIRCLE - diff
        if diff > MAX_BEAR_DIFF:
            return -1
        for cat in (Rating.EXCELLENT, Rating.GOOD, Rating.AVERAGE):
            if diff <= BEAR_INTERVALS[cat]:
                return BEAR_RATING[cat]
        return BEAR_RATING[Rating.POOR]

    def rating(self, lrp, line, dist):
        node_rating = self._distance_rating(dist)
        bear_rating = self._bear_rating(lrp.bear, line.bear)
        if bear_rating < 0:
            return -1

        line_rating = self._frc_rating(lrp.frc, line.frc) +\
            self._fow_rating(lrp.fow, line.fow) +\
            bear_rating

        return node_rating*NODE_FACTOR + line_rating*LINE_FACTOR

    def rating_details(self, lrp, line):
        details = self.RatingDetails(bear_rating=self._bear_rating(lrp.bear, line.bear),
                                     frc_rating=self._frc_rating(lrp.frc, line.frc),
                                     fow_rating=self._fow_rating(lrp.fow, line.fow))
        return details


def calculate_pairs(lines1, lines2, lastline, islastrp, islinelocation):
    """ Each LRP might have several candidate lines. In order to find the best
        pair to start with each pair needs to be investigated and rated. The
        rating process includes:

            - score of the first candidate line
            - score of the second candidate line
            - connection to the previously calculated path
            - candidate lines shall not be equal
    """
    # check connection with previously calculated path
    for l1, score1 in lines1:
        if lastline is not None and l1.id == lastline.id:
            score1 += CONNECT_ROUTE_INC * score1
        for l2, score2 in lines2:
            if not islastrp and islinelocation and l2.id == l1.id:
                score2 -= SAME_LINE_DEGRAD * score2
            yield (l1, l2), score1*score2


# Check for single line coverage
def singleline(candidates):
    bests = (lines[0] for lrp, lines in candidates)
    sl, _ = next(bests)
    for l, _ in bests:
        if l.id != sl.id:
            return None
    return sl


class ClassicDecoder(DecoderBase, RatingCalculator):
    """ OpenLR location decoder that use an abstract  map object

        See :py:class:`MapDatabase` for map database  interface.

    """
    def __init__(self, map_database,
                 max_node_distance=MAX_NODE_DIST,
                 frc_variance=FRC_VARIANCE,
                 dnp_variance=DNP_VARIANCE,
                 minimum_acc_rating=MIN_ACC_RATING,
                 find_lines_directly=True,
                 max_retry=MAX_NR_RETRIES,
                 verbose=False,
                 logger=lambda m: print(m)):
        """ Initialize the  decoder

            :param map_database: a map database instance
            :param max_node_distance: the maximun distance for candidate nodes
            :param frc_variance: allowed frc variances
            :param minimum_acc_rating: minimum acceptance rating for candidate lines
            :param find_lines_directly: enable direct search of candidate lines
                                    from lrp projection
            :param max_retry: maximum number of retry when searching for route
                between consecutive lines
        """
        self._mdb = map_database
        self._max_node_dist = max_node_distance
        self._frc_var = frc_variance
        self._min_acc_rating = minimum_acc_rating
        self._max_retry = max_retry
        self._dnp_variance = dnp_variance
        self.verbose = verbose
        self.find_lines_directly = find_lines_directly
        self.logger = logger

    @property
    def database(self):
        return self._mdb

    def find_candidate_nodes(self, lrp):
        """ Find candidate nodes for one location reference point.
            The max_node_distance configure the search for nodes being
            a possibility.
        """
        return self._mdb.find_closeby_nodes(lrp.coords, self._max_node_dist)

    def find_candidate_lines(self, lrp, beardir=WITH_LINE_DIRECTION, with_details=False):
        """ Find candidate lines for each location reference point. The candidate
            lines will be rated indicating how good they match the LRP attributes.
            The method will be configured by OpenLR properties.

            The connectedlines method takes a 'beardir' argument indicating
            inwards (AGAINST_LINE_DIRECTION) or outwards (WITH_LINE_DIRECTION) arcs
        """
        frc_max = lrp.frc + self._frc_var
        nodes = list(self.find_candidate_nodes(lrp))

        rating_f = self.rating
        min_acc = self._min_acc_rating

        rating_key = lambda l_r1: l_r1[1]
        group_key = lambda l_r2: l_r2[0].id

        candidates = ((l, rating_f(lrp, l, n.distance)) for n in nodes for l in self._mdb.connected_lines(
            n, frc_max=frc_max, beardir=beardir))
        if self.find_lines_directly:
            candidates = chain(candidates, self.find_candidate_lines_directly(
                lrp, frc_max=frc_max, alreadyfound=bool(nodes), beardir=beardir))
            candidates = (max(vals, key=rating_key) for k, vals in groupby(
                sorted(candidates, key=group_key), key=group_key))
        if not with_details:
            candidates = filter(lambda l_r: l_r[1] >= min_acc, candidates)
        lines = sorted(candidates, key=rating_key, reverse=True)
        if not with_details and not lines:
            raise DecoderNoCandidateLines("No candidate lines found....")

        if with_details:
            lines = [(l, r, self.rating_details(lrp, l)) for l, r, in lines]

        return lines

    def find_candidate_lines_directly(self, lrp, frc_max, alreadyfound=False, beardir=WITH_LINE_DIRECTION):
        """ Find candidate lines directly if no node or line has been detected so
            far. This method tries to find all lines which are around the LRP
            coordinate. The coordinate will be projected onto the line and the
            distance between that projection point and the coordinate shall be small
            (according to the encoder properties). All lines will be rated and
            proposed as candidate lines for the LRP.

            :param lrp: the location reference point (having no candidate lines so far)
            :param alreadyfound: the already found lines
        """
        rating_f = self.rating

        lines = self._mdb.find_closeby_lines(lrp.coords, self._max_node_dist, frc_max=frc_max, beardir=beardir)
        for line, dist in lines:
            rating = rating_f(lrp, line, dist)
            if alreadyfound:
                rating = round(LINES_DIRECTLY_FACTOR * rating)

            yield line, rating

    def resolve_route(self, location, candidates):
        """ Resolves the shortest-paths between each subsequent pair of location
            reference points. The method orders the candidate line pairs for two
            subsequent LRPs and starts with the best rated pair to calculate a
            shortest-path in between. The method further checks the minimum and
            maximum distance criteria for the calculated shortest-path. If one of the
            criteria is not fulfilled the methods tries the next best candidate line
            pair. If no further pair is available the method fails. For each
            subsequent pair of LRPs the start LRP will hold the calculated route
            after finishing this method.

            :param location: the location
            :param candidates: an iterable holding tuples of (lrp,candidate_lines)
        """

        if not isinstance(candidates, (list, tuple)):
            candidates = tuple(candidates)

        sl = singleline(candidates)
        if sl is not None:
            return (((sl,), sl.len),)

        islinelocation = (location.type == LocationType.LINE_LOCATION)

        lastlrp = location.llrp
        lastline, prevlrp = None, None

        routes = ()

        nr_retry = self._max_retry+1

        # iterate over all LRP pairs
        for i, (lrp, lines) in enumerate(candidates[:-1]):
            lrpnext, nextlines = candidates[i+1]
            islastrp = lrpnext is lastlrp
            pairs = sorted(calculate_pairs(lines, nextlines, lastline,
                           islastrp, islinelocation), key=lambda p_r: p_r[1], reverse=True)
            # check candidate pairs
            for (l1, l2), _ in pairs[:nr_retry]:
                if self.verbose:
                    self.logger("openlr: computing route ({},{})".format(l1.id, l2.id))
                # handle same start/end.
                if l1.id == l2.id:
                    if islastrp:
                        route = ((l1,), l1.len)
                    else:
                        # Skip this
                        route = EMPTY_ROUTE
                    break  # search finished
                try:
                    # calculate route between start and end and a maximum distance
                    route = self._calculate_route(l1, l2, lrp, islastrp)
                    # Handle change in start index
                    if lastline is not None and lastline.id != l1.id:
                        self._handle_start_change(routes, l1, lrp, prevlrp)
                    break  # search finished
                except (RouteNotFoundException, RouteConstructionFailed):
                    # Let a chance to retry
                    route = None

            if route is None:
                raise RouteNotFoundException("Route not found")

            if route is not EMPTY_ROUTE:
                routes += (route,)

            if self.verbose:
                # Display route
                lines, length = route
                self.logger("openlr: resolved route ({},{}):{} length={}".format(
                    l1.id, l2.id, tuple(l.id for l in lines), length))

            prevlrp, lastline = lrp, l2

        return routes

    def _handle_start_change(self, routes, lend, lrp, prevlrp):
        """ Recompute previous route using new end line
        """
        lstart, _ = routes[-1][0]
        if self.verbose:
            self.logger("openlr: recomputing last route between {} and {}".format(lstart.id, lend.id))
        route = self._calculate_route(lstart, lend, prevlrp, islastrp=False)
        routes = routes[:-1] + (route, )

    def _calculate_route(self, l1, l2, lrp, islastrp):
            """ Calculate shortest-path between two lines
            """
            # determine the minimum frc for the path to be calculated
            lfrc = lrp.lfrcnp + self._frc_var
            # Calculates the maximum allowed distance between two location reference
            # points taking into account that at least one LRP might be projected onto
            # a line and the maximum distance must be adjusted as the route calculation
            # can only stop at distances between real nodes.
            maxdist = lrp.dnp + self._dnp_variance
            # check if LRPs were projected on line (i.e obtained directly)
            # if yes, add line length to maxDistance (complete length as route
            # search stops at nodes)
            if l1.projected_len is not None:
                maxdist += l1.len
            if l2.projected_len is not None:
                maxdist += l2.len
            # calculate route between start and end and a maximum distance
            route, length = self._mdb.calculate_route(l1, l2, maxdist, lfrc, islastrp)
            # adjust and check the route length
            if l2.projected_len is not None:
                if islastrp:
                    length -= l2.len
                length += l2.projected_len
            # check the minimum distance criteria
            if max(0, lrp.dnp - self._dnp_variance) > length:
                raise InvalidRouteLength("openlr: route: {} to {}, calculated length:{}, lrp:{}".format(
                    l1.id, l2.id, length, lrp))

            return route, length

    def calculate_offsets(self, location, routes):
        # Compute offsets
        if location.version == BINARY_VERSION_2:
            return location.poffs, location.noffs
        elif location.version == BINARY_VERSION_3:
            (head, head_len), (tail, tail_len) = routes[0], routes[-1]

            head_start_line = head[0]
            cutstart = 0
            if head_start_line.projected_len is not None:
                cutstart = head_start_line.projected_len
                head_len -= cutstart

            tail_end_line = tail[-1]
            cutend = 0
            if tail_end_line.projected_len is not None:
                cutend = tail_end_line.len - tail_end_line.projected_len
                tail_len -= cutend

            if len(routes) == 1:
                head_len -= cutend
                tail_len -= cutstart
            else:
                # get the first line of the next sub-path
                head_end_line = (routes[1][0])[0]
                if head_end_line.projected_len is not None:
                    # there is another part on the first line of the next
                    # sub-path that relates to the head part
                    head_len += head_end_line.projected_len
                # get the first line of the last sub-path
                tail_start_line = tail[0]
                if tail_start_line.projected_len is not None:
                    # not everything of the tail belongs to it, there is a snippet
                    # at the start that refers to the former sub-path
                    tail_len -= tail_start_line.projected_len

            return (round(location.poffs * head_len / 100.0),
                    round(location.noffs * tail_len / 100.0))

    @staticmethod
    def _prune(pruned, off, index):
        prunedlen = 0
        while len(pruned) > 1:
            line = pruned[index]
            length = line.len
            if prunedlen + length > off:
                break
            else:
                prunedlen += length
                pruned.pop(index)
        return off - prunedlen

    @staticmethod
    def _calculated_path(pruned, poff, noff=0):
        length = sum(l.len for l in pruned)
        return [(l.id.uuid, l.id.is_reversed, l.is_reversed_in_database, l.len) for l in pruned], length, poff, noff

    def decode_line(self, location):
        """ Decode a line from a list of a location reference points

            return (edges, length, poffset, noffset)
        """
        # assert location.type == LocationType.LINE_LOCATION

        def candidates():
            yield location.flrp, self.find_candidate_lines(location.flrp)
            for lrp in location.points:
                yield lrp, self.find_candidate_lines(lrp)
            yield location.llrp, self.find_candidate_lines(location.llrp, AGAINST_LINE_DIRECTION)

        routes = self.resolve_route(location, candidates())
        poff, noff = self.calculate_offsets(location, routes)

        route_length = sum(length for _, length in routes)

        offsum = noff + poff
        # check for too long offset values
        if offsum >= 2*route_length:
            raise DecoderInvalidLocation("Invalid offsets")

        # prune path
        # The positive offset will be used to shorten the
        # location from the beginning and the negative offset will be used to
        # shorten the location from the end. <br>
        # The pruning will always stop at nodes and there will be no pruning of
        # parts of lines. The remaining offsets can be accessed from the returned
        # decoded location object. Remaining offsets which are below the length
        # variance parameter will be refused and set to 0

        if offsum > route_length:
            # offsets exceed location length
            # decrease offset values
            ratio = route_length / float(offsum)
            poff = round(poff * ratio)
            noff = round(noff * ratio)
            # retainable length shall be 1 meter
            if poff > noff:
                poff -= 1
            else:
                noff -= 1

        pruned = list(chain(*(lines for lines, _ in routes)))

        if poff > 0:
            poff = self._prune(pruned, poff, 0)
        if noff > 0:
            noff = self._prune(pruned, noff, -1)

        return self._calculated_path(pruned, poff, noff)

    def decode_point(self, location):
        """ Decode a point location from a couple of lrps
            return (edges, length, poffset)
        """
        # assert location.type in (LocationType.POINT_LOCATION_TYPES, LocationType.POI_WITH_ACCESS_POINT)

        routes = self.resolve_route(location, ((location.flrp, self.find_candidate_lines(location.flrp)),
                                   (location.llrp, self.find_candidate_lines(location.llrp, AGAINST_LINE_DIRECTION))))

        head, head_len = routes[0]
        lstart, lend = head[0], head[-1]

        prunedlen = 0
        poff = 0

        if lstart.projected_len is not None:
            poff = lstart.projected_len
            prunedlen = poff
        if lend.projected_len is not None:
            prunedlen += lend.len - lend.projected_len

        poff = round(location.poffs*(head_len-prunedlen)/100.0)+poff
        if poff > head_len:
            poff = head_len

        pruned = list(head)
        poff = self._prune(pruned, poff, 0)

        return self._calculated_path(pruned, poff)

    def decode(self, location):
        if location.type == LocationType.LINE_LOCATION:
            return self.decode_line(location)
        else:
            return self.decode_point(location)
