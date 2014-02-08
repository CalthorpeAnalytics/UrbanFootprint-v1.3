
__author__ = 'calthorpe'

class PlacetypeFixtures(object):

    simple_fixture = dict(
        Town_Commercial=dict(
            LandUse= [
                {
                           "category" :"Mixed-Use",
                           "percentage" :.21
                },
                {          "category" :"Residential",
                           "percentage" :0.0
                },
                {          "category" :"Jobs",
                           "percentage":0.34
                },
                {          "category" :"Civic",
                           "percentage":0.02
                },
                {          "category" : "Parks",
                           "percentage" :0.07
                },
                {          "category" :"Streets",
                           "percentage" :0.36
                }
            ],
            Residential= [
                {
                    "category" :"Multi-Family",
                    "percentage" :1.0
                },
                {          "category" :"Townhome",
                           "percentage" :0.0
                },
                {          "category" :"Single-Family Small Lot",
                           "percentage":0.0
                },
                {          "category" :"Single-Family Large Lot",
                           "percentage":0.00
                }
            ],
            Employment= [
                {
                    "category" :"Retail",
                    "percentage" :.09
                },
                {          "category" :"Office",
                           "percentage" :0.91
                },
                {          "category" :"Industrial",
                           "percentage":0.0
                }
            ]
        )
    )