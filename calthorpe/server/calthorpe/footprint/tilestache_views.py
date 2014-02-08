from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from footprint.models import TileStacheConfig


__author__ = 'calthorpe'

import TileStache


class LayerTypes(object):
    REFERENCE_LAYER = "reference"
    EDIT_LAYER = "editing"

    layer_types = dict(
        CensusBlockgroup=REFERENCE_LAYER,
        CensusBlock=REFERENCE_LAYER,
        CensusTract=REFERENCE_LAYER,

        ScagJurisdictionBoundaryFeature=REFERENCE_LAYER,
        ScagSphereOfInfluenceFeature=REFERENCE_LAYER,
        ScagTier1TazFeature=REFERENCE_LAYER,
        ScagTier2TazFeature=REFERENCE_LAYER,
        ScagParksOpenSpaceFeature=REFERENCE_LAYER,
        ScagTransitAreasFeature=REFERENCE_LAYER,
        ScagHabitatConservationAreasFeature=REFERENCE_LAYER,
        ScagFloodplainFeature=REFERENCE_LAYER,

        SacogStreamFeature=REFERENCE_LAYER,
        SacogWetlandFeature=REFERENCE_LAYER,
        SacogVernalPoolFeature=REFERENCE_LAYER,

        ScagPrimarySPZFeature=EDIT_LAYER,
        ScagGeneralPlanFeature=EDIT_LAYER,

        PrimaryParcelFeature=EDIT_LAYER,
        DevelopableFeature=EDIT_LAYER,

        CoreEndStateFeature=REFERENCE_LAYER,
        CoreGrossIncrementFeature=REFERENCE_LAYER,
        CoreIncrementFeature=REFERENCE_LAYER
    )


def tilestache_tiles(request, layer_name, z, x, y, extension):
    """
    :param request:
    :param layer_name:
    :param z:
    :param x:
    :param y:
    :param extension:
    :return:

    Proxy to tilestache
    {X} - coordinate column.
    {Y} - coordinate row.
    {B} - bounding box.
    {Z} - zoom level.
    {S} - host.
    """

    config = TileStacheConfig.objects.filter(name='default')[0].config
    path_info = "%s/%s/%s/%s.%s" % (layer_name, z, x, y, extension)
    coord, extension = TileStache.splitPathInfo(path_info)[1:]
    mimetype, content = TileStache.getTile(config.layers[layer_name], coord, extension)
    return HttpResponse(content, mimetype=mimetype)


def sample_charts(request):
    """
    Ofurhe's sample charts
    :param request:
    :return:
    """
    return direct_to_template(request, 'footprint/charts.html', {})