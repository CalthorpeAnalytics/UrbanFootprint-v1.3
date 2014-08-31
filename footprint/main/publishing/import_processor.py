
__author__ = 'calthorpe'


class ImportProcessor(object):
    """
        Describes the three methods of import.
        importer imports from a source
        peer importer imports from a peer DbEntity in the same ConfigEntity
        cloner copies from the same DbEntity of another ConfigEntity
    """
    def __init__(self, **kwargs):
        super(ImportProcessor, self).__init__()

    def importer(self, config_entity, db_entity):
        pass
    def peer_importer(self, config_entity, db_entity):
        pass
    def cloner(self, config_entity, db_entity):
        pass

