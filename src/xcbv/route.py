import six

from django.urls import URLPattern
from django.urls.resolvers import RoutePattern

from .exceptions import *


class RouteMetaclass(type):
    parent = None

    def factory(cls, **attributes):
        name = cls.__name__
        return type(name, (cls,), attributes)

    def __getattr__(cls, attr):
        if attr == 'namespace':
            return cls.get_namespace()
        if attr == 'app_name':
            return cls.get_app_name()
        if attr == 'name':
            return cls.get_name()
        if attr == 'path':
            return cls.get_path()
        if attr == 'model':
            if cls.parent:
                return cls.parent.model
            return None
        raise AttributeError(attr)

    def get_app_name(cls):
        if cls.parent:
            return cls.parent.app_name
        elif cls.model:
            return cls.model._meta.app_label

    def get_namespace(cls):
        if cls.parent:
            return cls.parent.namespace
        elif cls.model:
            return cls.model._meta.model_name

    def get_name(cls):
        name = cls.__name__.lower()
        if name.endswith('view'):
            name = name[:-4]
        elif name.endswith('route'):
            name = name[:-5]

        if cls.model:
            model_name = cls.model._meta.model_name.lower()
            if name.startswith(model_name):
                name = name[len(model_name):]

        if not name:
            raise RouteNameNotResolvable()
        return name

    def get_path(cls):
        try:
            return cls.name + '/'
        except RouteNameNotResolvable:
            raise RoutePathNotResolvable()

    @property
    def urlpattern(cls):
        return URLPattern(
            RoutePattern(cls.path, cls.namespace),
            cls.as_view(),
            name=cls.name,
        )


@six.add_metaclass(RouteMetaclass)
class Route(object):
    pass
