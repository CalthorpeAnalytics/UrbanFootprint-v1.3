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
from optparse import make_option
import logging

from django.core.management.base import BaseCommand

from footprint.models.config.scenario import FutureScenario
from footprint.models.presentation.layer_selection import DEFAULT_GEOMETRY, layer_selections_of_config_entity


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        This command clears all layer_selections
    """
    option_list = BaseCommand.option_list + (
        make_option('-r', '--resave', action='store_true', default=False,
                    help='Resave all the config_entities to trigger signals'),
        make_option('--scenario', default='', help='String matching a key of or more Scenario to run'),
    )

    def handle(self, *args, **options):
        scenarios = FutureScenario.objects.filter(key__contains=options['scenario']) if options[
            'scenario'] else FutureScenario.objects.all()
        for scenario in scenarios:
            for layer_selection in layer_selections_of_config_entity(scenario):
                # Set the bounds (performs a save)
                layer_selection.bounds = DEFAULT_GEOMETRY



