# coding=utf-8
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
from decimal import Decimal

__author__ = 'calthorpe_associates'


class Constants(object):
    USE_EFFICIENCY_DEFAULT = .85

    RESIDENTIAL_SQUARE_FEET_PER_DWELLING_UNIT = 1
    OFFICE_SQUARE_FEET_PER_EMPLOYEE = 1
    RETAIL_SQUARE_FEET_PER_EMPLOYEE = 1
    INDUSTRIAL_SQUARE_FEET_PER_EMPLOYEE = 1

    HH1_PERCENT = .4
    HH2_PERCENT = .2
    HH3_PERCENT = .2
    HH4_PERCENT = .1
    HH5P_PERCENT = .1

    AVERAGE_HH_SIZE = 2.5

    VACANCY_RATE = 0

    SQUARE_FEET_PER_ACRE = Decimal(43560.00000)
    PARKING_STALL_SQUARE_FEET =  Decimal(330.00000)