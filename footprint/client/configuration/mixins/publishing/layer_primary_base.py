from footprint.client.configuration.fixture import LandUseSymbologyFixture
from footprint.main.publishing.tilestache_style_configuration import create_template_context_dict_for_related_field
from footprint.client.configuration.utils import resolve_fixture
from footprint import settings

__author__ = 'calthorpe_associates'


def primary_base_template_context_dict(client_land_use_definition_class):
    # Resolve the client's specific color lookup for the PrimaryParcelFeature land_use_definition
    client_symbology = resolve_fixture(
        "publishing", "land_use_symbology", LandUseSymbologyFixture, settings.CLIENT)

    if not client_symbology:
        return

    color_lookup = client_symbology.land_use_color_lookup()

    # Create a default TemplateContext dict. This context will style the foreign key attribute of the LandUseDefinition
    return create_template_context_dict_for_related_field(
        'land_use_definition__id',
        client_land_use_definition_class,
        color_lookup,
        'land_use')
