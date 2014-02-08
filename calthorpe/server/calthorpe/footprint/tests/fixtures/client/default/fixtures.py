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

from footprint.initialization.fixture import FootprintFixture

from config_entity.config_entity_fixtures import config_entity
# Use the real built_form and policy fixtures
from footprint.initialization.fixtures.client.default.built_form.default_built_form import built_form
from footprint.initialization.fixtures.client.default.policy.default_policy import policy

footprint_fixture = FootprintFixture(
    config_entity=config_entity,
    built_form=built_form,
    policy=policy
)
