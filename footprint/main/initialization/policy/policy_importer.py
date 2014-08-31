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
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe
import csv
import os
from footprint.main.models import ResidentialEnergyBaseline, CommercialEnergyBaseline, EvapotranspirationBaseline
from footprint.settings import SERVER_ROOT


class PolicyImporter(object):
    def __init__(self):
        super(PolicyImporter, self).__init__()
        self.dir = os.path.dirname(__file__)

    def policy_path(self, client):
        # TODO Let the client resolve this via a fixture
        client_built_form_path = "{server_root}/footprint/client/configuration/{client}/policy/import_csv".format(
            server_root=SERVER_ROOT, client=client)

        return client_built_form_path

    def load_residential_energy_baseline_csv(self, client):
        """
        :param self.dir csv file self.directory
        :return: ImportedResidentialBaseline objects imported from UrbanFootprint v0.1 default set
        """
        path = '{0}/residential_energy_baselines.csv'.format(self.policy_path(client))
        if not os.path.exists(path):
            return []

        table = open(path, 'r')
        reader = csv.reader(table, delimiter=',', quotechar='"')

        for line in reader:
            if line[0] != 'zone':
                baseline = ResidentialEnergyBaseline()
                baseline.zone = line[0]
                baseline.du_detsf_ll_electricity = line[1]
                baseline.du_detsf_sl_electricity = line[2]
                baseline.du_attsf_electricity = line[3]
                baseline.du_mf_electricity = line[4]
                baseline.du_detsf_ll_gas = line[5]
                baseline.du_detsf_sl_gas = line[6]
                baseline.du_attsf_gas = line[7]
                baseline.du_mf_gas = line[8]
                baseline.save()

        table.close()

    def load_commercial_energy_baseline_csv(self, client):
        """
        :param self.dir csv file self.directory
        :return: ImportCommercialEnergyBaseline objects imported from UrbanFootprint v0.1 commercial baseline from
        default set, csv or a custom
        set defined for the client
        """
        path = '{0}/commercial_energy_baselines.csv'.format(self.policy_path(client))
        if not os.path.exists(path):
            return []

        table = open(path, 'r')
        reader = csv.reader(table, delimiter=',', quotechar='"')

        for line in reader:
            if line[0] != 'zone':
                baseline = CommercialEnergyBaseline()
                baseline.zone = line[0]
                baseline.retail_services_electricity = line[1]
                baseline.restaurant_electricity = line[2]
                baseline.accommodation_electricity = line[3]
                baseline.arts_entertainment_electricity = line[4]
                baseline.other_services_electricity = line[5]
                baseline.office_services_electricity = line[6]
                baseline.public_admin_electricity = line[7]
                baseline.education_electricity = line[8]
                baseline.medical_services_electricity = line[9]
                baseline.transport_warehousing_electricity = line[10]
                baseline.wholesale_electricity = line[11]
                baseline.retail_services_gas = line[12]
                baseline.restaurant_gas = line[13]
                baseline.accommodation_gas = line[14]
                baseline.arts_entertainment_gas = line[15]
                baseline.other_services_gas = line[16]
                baseline.office_services_gas = line[17]
                baseline.public_admin_gas = line[18]
                baseline.education_gas = line[19]
                baseline.medical_services_gas = line[20]
                baseline.transport_warehousing_gas = line[21]
                baseline.wholesale_gas = line[22]
                baseline.save()

        table.close()


    def load_outdoor_water_baseline_csv(self, client):
        """
        :param self.dir csv file self.directory
        :return: ImportedResidentialBaseline objects imported from UrbanFootprint v0.1 default set
        """
        path = '{0}/outdoor_water_baselines.csv'.format(self.policy_path(client))
        if not os.path.exists(path):
            return []

        table = open(path, 'r')
        reader = csv.reader(table, delimiter=',', quotechar='"')

        for line in reader:
            if line[0] != 'zone':
                baseline = EvapotranspirationBaseline()
                baseline.zone = line[0]
                baseline.annual_evapotranspiration = line[1]
                baseline.save()

        table.close()

