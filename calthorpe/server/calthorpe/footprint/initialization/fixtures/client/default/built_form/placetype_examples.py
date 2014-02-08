import json

__author__ = 'calthorpe'
placetype_example_json = """{

        "pt__town_commercial" : [
            {
                "example_name"        : "Downtown Ashland",
                "example_url"         : "http://www.ashland.or.us/"
            },
            {
                "example_name"        : "Downtown Redwood City",
                "example_url"         : "http://www.redwoodcity.org/"
            }

        ],
        "pt__campus_university" : [
            {
                "example_name"  : "University of California, Berkeley",
                "example_url"   : "http://www.berkeley.edu/index.html"
            },
            {
                "example_name"  : "University of Oregon",
                "example_url"   : "http://uoregon.edu/"
            }

        ],
        "default" : [
            {
                "example_name"  : "Placetype example region 1",
                "example_url"   : "http://www.berkeley.edu/index.html"
            },
            {
                "example_name"  : "Placetype example region 2",
                "example_url"   : "http://uoregon.edu/"
            }

        ]
    }"""
PLACETYPE_EXAMPLES = json.loads(placetype_example_json)


