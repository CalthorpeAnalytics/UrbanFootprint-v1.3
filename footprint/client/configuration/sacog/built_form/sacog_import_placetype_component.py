__author__ = 'calthorpe_associates'

from csvImporter.fields import CharField, FloatField, IntegerField
from csvImporter.model import CsvModel


class ImportPlacetypeComponent(CsvModel):
#    BTID,Building_Type,
# Urban Mixed Use,Urban Residential,Urban Commercial,City Mixed Use,City Residential,City Commercial,
# Town Mixed Use,Town Residential,Town Commercial,Village Mixed Use,Village Residential,Village Commercial,
# Neighborhood Residential,Neighborhood Low,Office Focus,Mixed Office and R&D,Office/Industrial,Industrial Focus,
# Low-Density Employment Park,High Intensity Activity Center,Mid Intensity Activity Center,
# Low Intensity Retail-Centered N'Hood,Retail: Strip Mall/ Big Box,Industrial/Office/Res Mixed High,
# Industrial/Office/Res Mixed Low,Suburban Multifamily,Suburban Mixed Residential,Residential Subdivision,
# Large Lot Residential Area,Rural Residential,Rural Ranchettes,Rural Employment,Campus/ University,
# Institutional,Parks & Open Space,BuildingType Name,Gross_Net_Flag
    category = CharField(prepare=lambda x: x or '')
    btid = IntegerField(prepare=lambda x: x or 0)
    color = CharField(prepare=lambda x: x or '')
    name = CharField(prepare=lambda x: x or '')

    class Meta:
        delimiter = ","
        has_header = True

CROP_TYPES = {
    "Tomato Rotation": {
        "Alfalfa": .194,
        "Beans": 0.003,
        "Corn": 0.038,
        "PTomatoes": .456,
        "Safflower": .047,
        "Sunflower": .066,
        "Wheat": .196,
    },
    "Alfalfa Rotation": {
        "Alfalfa": .596,
        "Beans": 0.002,
        "Corn": 0.066,
        "Safflower": .033,
        "Sunflower": .067,
        "Wheat": .236,
    },
    "General Field Crops": {
        "Alfalfa": .452,
        "Beans": .009,
        "Corn": .045,
        "Safflower": .130,
        "Sunflower": .093,
        "Wheat": .271
    },
    "Grain/Other Vegetable Rotation":
    {
        "Alfalfa": .452,
        "Beans": .009,
        "Corn": .045,
        "Safflower": .130,
        "Sunflower": .093,
        "Wheat": .271
    },
    "Rice Rotation": {
        'Alfalfa': .038,
        'Corn': .016,
        'Wheat': .10,
        'Safflower': .02,
        'Sunflower': .003,
        'Beans': .016,
        'PTomatoes': .061,
        'Rice': .608,
        'Fallow': .118,
        'Pasture/Rangeland': .2
    }
}
