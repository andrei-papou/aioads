from extensions.bl_exceptions import DefaultMessageException


class AdvertOrderForSuchLinkAlreadyExists(DefaultMessageException):
    default_message = 'Advert order for such follow_url_link already exists'
