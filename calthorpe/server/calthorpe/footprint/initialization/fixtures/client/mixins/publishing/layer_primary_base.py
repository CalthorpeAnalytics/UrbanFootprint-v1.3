from footprint.initialization.fixture import LandUseSymbologyFixture
from footprint.initialization.publishing.tilestache_style_configuration import create_template_context_dict_for_foreign_key
from footprint.initialization.utils import resolve_fixture
import settings

__author__ = 'calthorpe'


def primary_base_template_context_dict(client_primary_base_feature_class):
    # Resolve the client's specific color lookup for the PrimaryParcelFeature land_use_definition
    client_symbology = resolve_fixture(
        "publishing", "land_use_symbology", LandUseSymbologyFixture, settings.CLIENT)

    if not client_symbology:
        return

    color_lookup = client_symbology.land_use_color_lookup()

    model_field = client_primary_base_feature_class._meta.get_field_by_name('land_use_definition')[0]

    # Create a default TemplateContext dict. This context will style the foreign key attribute of the LandUseDefinition
    return create_template_context_dict_for_foreign_key(
        model_field,
        color_lookup,
        'land_use')
