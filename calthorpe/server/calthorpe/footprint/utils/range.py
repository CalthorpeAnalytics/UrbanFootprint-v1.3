# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
# 
# Copyright (C) 2012 Calthorpe Associates
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# 
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com

__author__ = 'calthorpe'

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def length(self):
        return self.end - self.start

    def overlaps(self, other):
        return not(self.end < other.start or other.end < self.start)

    def name(self):
        return '_'.join([str(self.start), str(self.end)])

    def __unicode__(self):
        return u'%s' % self.name()

    def __str__(self):
        return self.__unicode__().encode('utf-8')


def make_ranges(min, max, count, explicit_increments=[]):
    full_range = max-min
    increment = full_range/count
    if len(explicit_increments) > 0:
        if len(explicit_increments)+1 != count:
            raise Exception("explicit_increments count ({0}) is not one less than count ({1})".format(len(explicit_increments), count))
        all_increments = [min]+explicit_increments+[max]
        return map(lambda index: Range(all_increments[index], all_increments[index+1]), range(len(all_increments)-1))
    else:
        return map(lambda index: Range(min+increment*index, min+increment*(index+1)), range(count))

# Complements make_ranges by creating a sequences of values between and including min and max
def make_increments(min, max, count):
    full_range = max-min
    # Decrease the count so that our last increment is max
    increment = full_range/count-1
    # Creates a sequence starting a min and ending at max, with intermediates equidistant
    return map(lambda index: min+increment*index, range(count))
