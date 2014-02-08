from footprint.main.lib.functions import map_to_dict
from footprint.main.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


class BuiltFormDerivatives(object):
    def construct_primary_component_percents(self, placetype_components, primary_components, client):
        """
        :return: BuildingPercent objects (UrbanFootprint v0.1 Built Form default set)
        """
        primary_components = []
        import_primary_components = self.load_buildings_csv(client)
        for import_primary_component in import_primary_components:
            primary_component = dict(
                primary_component_name=import_primary_component.name,
                primary_component=import_primary_component,
                placetype_component_name=import_primary_component.placetype_component,
                placetype_component=placetype_components[import_primary_component.placetype_component],
                percent=import_primary_component.percent_of_placetype_component
            )
            primary_components.append(primary_component)
        return primary_components

    def construct_building_use_percents(self, primary_components, client):
        """
        :return: BuildingUsePercent objects (UrbanFootprint v0.1 Built Form default set)
        """
        building_use_percents = []

        def make_building_use_percent_dict(import_primary_component, building_use, building_use_category):
            """
            uses the building_use_category to populate the sub-categories of building uses with
            efficiency, square_feet_per_unit, and vacancy_rate
            """
            if building_use == 'Armed Forces':
                return None
            import_use_field = building_use.lower().replace(' ', '_')
            import_use_category_field = building_use_category.lower().replace(' ', '_')
            use_percent = getattr(import_primary_component, 'percent_{0}'.format(import_use_field))
            if use_percent > 0:

                vacancy_rate = getattr(import_primary_component, 'vacancy_rate', 0)
                efficiency = getattr(import_primary_component, '{0}_efficiency'.format(import_use_category_field), .85)
                square_feet_per_unit = getattr(import_primary_component,
                                               '{0}_square_feet_per_unit'.format(import_use_category_field), 10000)

                building_uses = dict(
                    vacancy_rate=vacancy_rate,
                    building_use_definition=BuildingUseDefinition.objects.get_or_create(name=building_use)[0],
                    percent=use_percent,
                    efficiency=efficiency,
                    square_feet_per_unit=square_feet_per_unit,
                )

                if import_primary_component.household_size > 0:
                    building_uses['household_size'] = import_primary_component.household_size

                building_use_percent = dict(
                    built_form_dict=primary_component,
                    built_form_name=primary_component['building_attributes']['name'],
                    built_form_uses=building_uses
                )

                return building_use_percent

        for import_primary_component in self.load_buildings_csv(client):

            primary_component = primary_components[import_primary_component.name]
            for building_use, building_use_category in Keys.BUILDING_USE_DEFINITION_CATEGORIES.items():
                building_use_percent = make_building_use_percent_dict(import_primary_component, building_use,
                                                                      building_use_category)
                if building_use_percent:
                    building_use_percents.append(building_use_percent)
                del building_use_percent

        return building_use_percents

    def construct_placetype_component_percents(self, placetype_dict, placetype_component_dict, client):
        """
        :return:
        """

        import_placetype_components = [placetype_component for placetype_component in self.load_buildingtype_csv(client)]

        input_placetypes = self.load_placetype_csv(client)
        input_placetype_dict = map_to_dict(lambda input_placetype: [input_placetype.name, input_placetype],
                                           input_placetypes)
        placetype_component_dict = dict()

        for name, placetype in placetype_dict.items():
            placetype_name = placetype['building_attributes']['name'].strip()

            for input_placetype_component in import_placetype_components:

                placetype_component_percent = getattr(input_placetype_component,
                                                      input_placetype_dict[placetype_name].clean_name)

                placetype_component_name = input_placetype_component.name.strip()

                default_placetype_component_dict = dict()

                placetype_component_dict[placetype_name] = placetype_component_dict.get(placetype_name,
                                                                                      default_placetype_component_dict)

                if placetype_component_percent > 0:
                    category = input_placetype_component.category.strip()
                    if category:
                        placetype_component_dict[placetype_name][placetype_component_name] = {
                            'category': category,
                            'percent': placetype_component_percent,
                        }

        return placetype_component_dict
