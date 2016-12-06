from extensions.bl_exceptions import DefaultMessageException


class PlacementDoesNotExist(DefaultMessageException):
    default_message = 'Placement does not exist'


class AttemptToGetForeignClicks(DefaultMessageException):
    default_message = 'Attempt to fetch clicks data which belongs to someone else'
