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
from django.core.management import call_command
from django.template.defaultfilters import slugify

from footprint.initialization.fixture import BuiltFormFixture, LandUseSymbologyFixture
from footprint.initialization.fixtures.client.scag.built_form.scag_land_use import ScagLandUse
from footprint.initialization.fixtures.client.scag.built_form.scag_land_use_definition import ScagLandUseDefinition
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import merge
from footprint.mixins.tag import Tag
from footprint.models.built_form.built_form import update_or_create_built_form_medium
import settings


class ScagBuiltFormFixture(BuiltFormFixture):
    def built_forms(self):
        def construct_scag_land_uses():
            if ScagLandUseDefinition.objects.count() == 0:
                # TODO throw if this errs
                call_command('loaddata',
                             'footprint/initialization/fixtures/client/scag/built_form/scag_land_use_definitions.json')

            land_use_symbology_fixture = resolve_fixture(
                "publishing",
                "land_use_symbology",
                LandUseSymbologyFixture,
                settings.CLIENT)
            land_use_lookup = land_use_symbology_fixture.land_use_color_lookup()
            return map(
                lambda land_use_definition: ScagLandUse.objects.update_or_create(
                    key='scg_lu__' + slugify(land_use_definition.land_use_description).replace('-', ','),
                    defaults=dict(
                        land_use_definition=land_use_definition,
                        name=land_use_definition.land_use_description,
                        medium=update_or_create_built_form_medium(
                            'scag_land_use_%s' % land_use_definition.land_use,
                            land_use_lookup.get(str(land_use_definition.land_use), None)
                        )
                    ))[0],
                ScagLandUseDefinition.objects.all())

        return merge(
            self.parent_fixture.built_forms(),
            dict(scag_land_use=construct_scag_land_uses()))

    def tag_built_forms(self, built_forms_dict):
        self.parent_fixture.tag_built_forms(built_forms_dict),
        # Give client built_forms a default tag if they don't have any tag yet
        Tag.objects.update_or_create(tag='Unsorted')
        for built_form in built_forms_dict['scag_land_use']:
            if built_form.tags.count() == 0:
                tag, created, updated = Tag.objects.update_or_create(
                    tag=built_form.land_use_definition.land_use_type or 'Unsorted')
                built_form.tags.add(tag)

    def built_form_sets(self):
        return self.parent_fixture.built_form_sets() + [dict(
            key='scag_land_use',
            name='Land Use:SCAG',
            client='scag',
            description='ScagLandUse containing only scag_land_uses',
            clazz=ScagLandUse
        )]
