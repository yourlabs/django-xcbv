from .exceptions import *

import six


class RouteMetaclass(type):
    parent = None

    def factory(cls, **attributes):
        name = cls.__name__
        return type(name, (cls,), attributes)

    def __getattr__(cls, attr):
        if attr == 'namespace' and cls.parent:
            return cls.parent.namespace
        if attr == 'app_name' and cls.parent:
            return cls.parent.app_name
        if attr == 'name':
            return cls.get_name()
        if attr == 'path':
            return cls.get_path()
        raise AttributeError(attr)

    def get_name(cls):
        name = cls.__name__.lower()
        if name.endswith('view'):
            name = name[:-4]
        elif name.endswith('route'):
            name = name[:-5]
        if not name:
            raise RouteNameNotResolvable()
        return name

    def get_path(cls):
        try:
            return cls.name + '/'
        except RouteNameNotResolvable:
            raise RoutePathNotResolvable()


@six.add_metaclass(RouteMetaclass)
class Route(object):
    pass
