from .exceptions import *

import six


class RouteMetaclass(type):
    name = None
    parent = None

    def factory(cls, **attributes):
        name = cls.__name__
        return type(name, (cls,), attributes)

    def __getattr__(cls, attr):
        if attr == 'namespace' and cls.parent:
            return cls.parent.namespace
        if attr == 'app_name' and cls.parent:
            return cls.parent.app_name
        if attr == 'path':
            return cls.get_path()
        raise AttributeError(attr)

    def get_path(cls):
        if cls.name:
            return cls.name + '/'
        raise RoutePathNotResolvable()


@six.add_metaclass(RouteMetaclass)
class Route(object):
    pass
