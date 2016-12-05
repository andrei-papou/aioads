from extensions.bl_exceptions import DefaultMessageException


class PlacementDoesNotExist(DefaultMessageException):
    default_message = 'Placement does not exist'
