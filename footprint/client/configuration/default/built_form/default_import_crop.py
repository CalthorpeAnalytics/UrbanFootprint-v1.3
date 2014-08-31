# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

from csvImporter.fields import CharField, FloatField, IntegerField
from csvImporter.model import CsvModel


class ImportCrop(CsvModel):
    id = IntegerField(prepare=lambda x: x or 0)
    name = CharField(prepare=lambda x: x or '')

    crop_yield = FloatField(prepare=lambda x: x or 0)
    unit_price = FloatField(prepare=lambda x: x or 0)
    cost = FloatField(prepare=lambda x: x or 0)
    water_consumption = FloatField(prepare=lambda x: x or 0)
    labor_input = FloatField(prepare=lambda x: x or 0)
    truck_trips = FloatField(prepare=lambda x: x or 0)

    class Meta:
        delimiter = ","
        has_header = True

class ImportCropType(CsvModel):
    id = IntegerField(prepare=lambda x: x or 0)
    name = CharField(prepare=lambda x: x or '')
    alfalfa = FloatField(prepare=lambda x: x or 0)
    almonds = FloatField(prepare=lambda x: x or 0)
    apples = FloatField(prepare=lambda x: x or 0)
    apricots = FloatField(prepare=lambda x: x or 0)
    asparagus = FloatField(prepare=lambda x: x or 0)
    beans = FloatField(prepare=lambda x: x or 0)
    blueberries = FloatField(prepare=lambda x: x or 0)
    corn = FloatField(prepare=lambda x: x or 0)
    grapes = FloatField(prepare=lambda x: x or 0)
    mandarins = FloatField(prepare=lambda x: x or 0)
    nursery = FloatField(prepare=lambda x: x or 0)
    olives = FloatField(prepare=lambda x: x or 0)
    other_citrus = FloatField(prepare=lambda x: x or 0)
    other_fruits_and_nuts = FloatField(prepare=lambda x: x or 0)
    other_stone_fruits = FloatField(prepare=lambda x: x or 0)
    pasture = FloatField(prepare=lambda x: x or 0)
    peaches = FloatField(prepare=lambda x: x or 0)
    pears = FloatField(prepare=lambda x: x or 0)
    prunes = FloatField(prepare=lambda x: x or 0)
    rice = FloatField(prepare=lambda x: x or 0)
    safflower = FloatField(prepare=lambda x: x or 0)
    strawberry = FloatField(prepare=lambda x: x or 0)
    sunflower = FloatField(prepare=lambda x: x or 0)
    timber = FloatField(prepare=lambda x: x or 0)
    tomatoes = FloatField(prepare=lambda x: x or 0)
    vegetables = FloatField(prepare=lambda x: x or 0)
    walnuts = FloatField(prepare=lambda x: x or 0)
    wheat = FloatField(prepare=lambda x: x or 0)
