

class xcbvException(Exception):
    pass


class RouterNamespaceNotResolvable(xcbvException):
    pass


class NamespaceCollision(xcbvException):
    pass