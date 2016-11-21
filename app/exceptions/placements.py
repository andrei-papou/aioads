from extensions.bl_exceptions import DefaultMessageException


class AdvertOrderDoesNotExist(DefaultMessageException):
    default_message = 'Advert order with such id does not exist'


class DuplicatedPlacement(DefaultMessageException):
    default_message = 'This ad placer already has already placed this advert'
