from extensions.bl_exceptions import DefaultMessageException


class AdvertOrderForSuchLinkAlreadyExists(DefaultMessageException):
    default_message = 'Advert order for such follow_url_link already exists'


class AnotherUserOrderUpdateAttempt(DefaultMessageException):
    default_message = 'You can\'t update another user\'s order'


class AnotherUserOrderDeleteAttempt(DefaultMessageException):
    default_message = 'You can\'t delete another user\'s order'


class AdvertOrderDoesNotExist(DefaultMessageException):
    default_message = 'Advert order with such id does not exist'
