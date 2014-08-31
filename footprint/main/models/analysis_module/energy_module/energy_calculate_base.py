from footprint.main.models.analysis_module.energy_module.energy_keys import ENERGY_TYPES, RESIDENTIAL_TYPES, COMMERCIAL_TYPES

__author__ = 'calthorpe'




def  calculate_base_energy(energy_dict):

    for energy_type in ENERGY_TYPES:

        energy_dict['residential_{0}_use'.format(energy_type)] = float(0)
        energy_dict['commercial_{0}_use'.format(energy_type)] = float(0)

        types = RESIDENTIAL_TYPES + COMMERCIAL_TYPES

        for type in types:
            energy_dict['{0}_{1}_use'.format(type, energy_type)] = \
                energy_dict['{0}'.format(type)] * \
                energy_dict['{0}_{1}'.format(type, energy_type)]

        for type in RESIDENTIAL_TYPES:
            energy_dict['residential_{0}_use'.format(energy_type)] = \
                energy_dict['residential_{0}_use'.format(energy_type)] + \
                energy_dict['{0}_{1}_use'.format(type, energy_type)]

        for type in COMMERCIAL_TYPES:
            energy_dict['commercial_{0}_use'.format(energy_type)] = \
                energy_dict['commercial_{0}_use'.format(energy_type)] +  \
                energy_dict['{0}_{1}_use'.format(type, energy_type)]

        energy_dict['total_{0}_use'.format(energy_type)] = \
            energy_dict['residential_{0}_use'.format(energy_type)] + \
            energy_dict['commercial_{0}_use'.format(energy_type)]

    return energy_dict