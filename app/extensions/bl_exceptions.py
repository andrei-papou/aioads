class MessageException(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message


class DefaultMessageException(MessageException):
    default_message = None

    def __init__(self, message=None):
        msg = message or self.default_message
        super().__init__(msg)
