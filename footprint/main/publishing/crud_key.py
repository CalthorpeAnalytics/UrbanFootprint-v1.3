from footprint.main.mixins.cloneable import Cloneable
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe'

class CrudKey(Keys):
    CREATE = 'create'
    CLONE = 'clone'
    UPDATE = 'update'
    SYNC = 'sync'
    DELETE = 'delete'

    @staticmethod
    def resolve_crud(**kwargs):
        """
            Resolves the desired CRUD operation to CrudKey.CREATE|CLONE|UPDATE|SYNC|DELETE
            The default value is CrudKey.UPDATE. kwargs['created'] resolves to CrudKey.CREATE or CLONE--
            the latter only in the instance is Cloneable and has an origin_instance.
            SYNC and DELETE are returned if the 'sync' or 'deleted' kwargs are set True, respectively.
            :param kwargs: contains 'instance' and optionally 'created', 'deleted', and 'sync'
        """
        instance = kwargs['instance']
        if kwargs.get('sync'):
            return CrudKey.SYNC
        if kwargs.get('created'):
            if isinstance(instance, Cloneable) and instance.origin_instance:
                return CrudKey.CLONE
            else:
                return CrudKey.CREATE
        if kwargs.get('deleted'):
            return CrudKey.DELETE
        else:
            return CrudKey.UPDATE

