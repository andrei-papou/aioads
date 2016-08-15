from extensions.bl_exceptions import DefaultMessageException


class EmailAlreadyInUse(DefaultMessageException):
    default_message = 'The email supplied is already in use'


class WebsiteAlreadyRegistered(DefaultMessageException):
    default_message = 'The account for such a website is already registered'


class UserDoesNotExist(DefaultMessageException):
    default_message = 'User with the email provided does not exist'


class InvalidPassword(DefaultMessageException):
    default_message = 'The password provided is invalid'
