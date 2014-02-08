__author__ = 'calthorpe'

# Import all client models that have static tables so that we have a single migration path
from footprint.client.configuration.fixture import InitFixture
from footprint.client.configuration.utils import resolve_fixture, resolve_client_module
from footprint import settings

# Load all client modules into the system, even though we only will configure one CLIENT
# This forces South to create all client specific table definitions
for client in settings.ALL_CLIENTS:
    client_init = resolve_fixture(None, "init", InitFixture, client)
    #client_init.import_database()
    for module_tuple in client_init.model_class_modules():
        # Load the module so that Django and South find the classes
        resolve_client_module(module_tuple[0], module_tuple[1], client)

