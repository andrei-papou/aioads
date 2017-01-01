from extensions.bl_exceptions import DefaultMessageException


class AdvertOrderDoesNotExist(DefaultMessageException):
    default_message = 'Advert order with such id does not exist'


class DuplicatedPlacement(DefaultMessageException):
    default_message = 'This ad placer already has already placed this advert'


class PlacementDoesNotExist(DefaultMessageException):
    default_message = 'Placement with such id does not exist'


class AttemptToRemoveForeignPlacement(DefaultMessageException):
    default_message = 'Attempt to remove foreign placement'


class AttemptToGetForeignPlacement(DefaultMessageException):
    default_message = 'Attempt to get foreign placement'
