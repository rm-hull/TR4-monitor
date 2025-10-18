# Copyright 2008-2016 by Carnegie Mellon University
# See license information in LICENSE-OPENSOURCE.txt

"""
A set of functions to produce ranges of aesthetically-pleasing numbers
that have the specified length and include the specified range.
Functions are provided for producing nice numeric and time-based
ranges.
"""

from __future__ import division
import math

#
# Regular number stuff (code mutated from original work by Katherine
# Prevost)
#


nice_intervals = [1.0, 2.0, 2.5, 3.0, 5.0, 10.0]
int_intervals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
int_12_intervals = [1.0, 2.0, 3.0, 4.0, 6.0, 12.0]
int_60_intervals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 10.0, 12.0, 15.0, 20.0, 30.0]


def nice_ceil(x, intervals=nice_intervals, base=10.0):
    if x == 0:
        return 0
    if x < 0:
        return nice_floor(x * -1, intervals, base) * -1
    z = base ** math.floor(math.log(x, base))
    for i in range(len(intervals) - 1):
        result = intervals[i] * z
        if x <= result:
            return result
    return intervals[-1] * z


def nice_floor(x, intervals=nice_intervals, base=10.0):
    if x == 0:
        return 0
    if x < 0:
        return nice_ceil(x * -1, intervals, base) * -1
    z = base ** (math.ceil(math.log(x, base)) - 1.0)
    for i in range(len(intervals) - 1, 1, -1):
        result = intervals[i] * z
        if x >= result:
            return result
    return intervals[0] * z


def nice_round(x, intervals=nice_intervals, base=10.0):
    if x == 0:
        return 0
    z = base ** (math.ceil(math.log(x, base)) - 1.0)
    for i in range(len(intervals) - 1):
        result = intervals[i] * z
        cutoff = (result + intervals[i + 1] * z) / 2.0
        if x <= cutoff:
            return result
    return intervals[-1] * z


def nice_ticks(lo, hi, ticks=5, inside=False, intervals=nice_intervals, base=10.0):
    """
    Find 'nice' places to put *ticks* tick marks for numeric data
    spanning from *lo* to *hi*.  If *inside* is ``True``, then the
    nice range will be contained within the input range.  If *inside*
    is ``False``, then the nice range will contain the input range.
    To find nice numbers for time data, use :func:`nice_time_ticks`.

    The result is a tuple containing the minimum value of the nice
    range, the maximum value of the nice range, and an iterator over
    the tick marks.

    See also :func:`nice_ticks_seq`.
    """

    if lo > hi:
        value_error = ValueError("Low value greater than high value: %r, %r" % (lo, hi))
        raise value_error

    delta_x = hi - lo
    if delta_x == 0:
        lo = nice_floor(lo, intervals, base)
        hi = nice_ceil(hi, intervals, base)
        delta_x = hi - lo
        if delta_x == 0:
            lo = lo - 0.5
            hi = hi + 0.5
            delta_x = hi - lo

    delta_t = nice_round(delta_x / (ticks - 1), intervals, base)
    if inside:
        lo_t = math.ceil(lo / delta_t) * delta_t
        hi_t = math.floor(hi / delta_t) * delta_t
    else:
        lo_t = math.floor(lo / delta_t) * delta_t
        hi_t = math.ceil(hi / delta_t) * delta_t

    def t_iter():
        t = lo_t
        while t <= hi_t:
            yield t
            t = t + delta_t

    return (lo_t, hi_t, t_iter())


def nice_ticks_seq(lo, hi, ticks=5, inside=False):
    """
    A convenience wrapper of :func:`nice_ticks` to return the nice
    range as a sequence.
    """
    return tuple(nice_ticks(lo, hi, ticks, inside)[2])
