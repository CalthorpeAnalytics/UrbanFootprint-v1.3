from footprint.main.models.geospatial.feature import Feature
from django.db import models

__author__ = 'calthorpe_associates'


class BaseDemographicFeature(Feature):

    du_occupancy_rate = models.DecimalField(max_digits=14, decimal_places=4)
    pop_male = models.DecimalField(max_digits=14, decimal_places=4)
    pop_female = models.DecimalField(max_digits=14, decimal_places=4)

    pop_avg_age20_64 = models.DecimalField(max_digits=14, decimal_places=4)

    pop_female_age20_64 = models.DecimalField(max_digits=14, decimal_places=4)
    pop_male_age20_64 = models.DecimalField(max_digits=14, decimal_places=4)

    pop_age16_up = models.DecimalField(max_digits=14, decimal_places=4)
    pop_age25_up = models.DecimalField(max_digits=14, decimal_places=4)
    pop_age65_up = models.DecimalField(max_digits=14, decimal_places=4)

    pop_age20_64 = models.DecimalField(max_digits=14, decimal_places=4)
    pop_hs_not_comp = models.DecimalField(max_digits=14, decimal_places=4)
    pop_hs_diploma = models.DecimalField(max_digits=14, decimal_places=4)
    pop_some_college = models.DecimalField(max_digits=14, decimal_places=4)
    pop_college_degree = models.DecimalField(max_digits=14, decimal_places=4)
    pop_graduate_degree = models.DecimalField(max_digits=14, decimal_places=4)
    pop_employed = models.DecimalField(max_digits=14, decimal_places=4)

    hh_inc_00_10 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_10_20 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_20_30 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_30_40 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_40_50 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_50_60 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_60_75 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_75_100 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_100_125 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_125_150 = models.DecimalField(max_digits=14, decimal_places=4)

    hh_inc_150_200 = models.DecimalField(max_digits=14, decimal_places=4)
    hh_inc_200p = models.DecimalField(max_digits=14, decimal_places=4)
    hh_avg_vehicles = models.DecimalField(max_digits=14, decimal_places=4)
    hh_avg_size = models.DecimalField(max_digits=14, decimal_places=4)
    hh_agg_inc = models.DecimalField(max_digits=14, decimal_places=4)
    hh_avg_inc = models.DecimalField(max_digits=14, decimal_places=4)
    hh_owner_occ = models.DecimalField(max_digits=14, decimal_places=4)
    hh_rental_occ = models.DecimalField(max_digits=14, decimal_places=4)

    class Meta(object):
        abstract = True
        app_label = 'main'
