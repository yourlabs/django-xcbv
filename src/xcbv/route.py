from itertools import chain
import six

from django.views.generic import View
from django.urls import URLPattern, URLResolver, path
from django.urls.resolvers import RegexPattern, RoutePattern

from .exceptions import *


class RouteMetaclass(type):
    parent = None
    routes = []
    lazy_classproperties = [
        'app_name',
        'model',
        'name',
        'namespace',
        'pattern',
        'regex',
    ]

    def factory(cls, *routes, **attributes):
        name = cls.__name__
        model = attributes.get('model', None)
        if model and model.__name__ not in name:
            name = model.__name__ + name
        cls = type(name, (cls,), attributes)
        cls.routes_init(routes)
        return cls

    def __getattr__(cls, attr):
        if attr in cls.lazy_classproperties:
            return getattr(cls, 'get_' + attr)()
        raise AttributeError(attr)

    def get_model(cls):
        if cls.parent:
            return cls.parent.model
        return None

    def get_app_name(cls):
        if cls.parent:
            return cls.parent.app_name
        elif cls.model:
            return cls.model._meta.app_label

    def get_namespace(cls):
        if cls.model:
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

        if not name and cls.model:
            name = cls.model._meta.model_name

        return name or None

    def get_regex(cls):
        r = ''
        if 'name' in dir(cls):
            r += cls.name
        elif cls.model:
            r += cls.model._meta.model_name
        else:
            r += cls.name

        return r

    def get_path(cls):
        return None

    def routes_init(cls, routes):
        cls.routes = [
            route.factory(parent=cls)
            for route in list(cls.routes) + list(routes)
        ]

        namespaces = []
        for route in cls.routes:
            if not route.namespace:
                continue
            if route.routes:
                continue
            if route.namespace in namespaces:
                raise NamespaceCollision(route.namespace)
            namespaces.append(route.namespace)

    @property
    def urlpattern(cls):
        return path(cls.regex, cls.as_view(), name=cls.name)

    def urlpatterns(cls, with_self=True):
        patterns = []

        if with_self:
            patterns.append(cls.urlpattern)

        sub_patterns = []
        for r in cls.routes:
            sub_patterns += r.urlpatterns()

        patterns.append(path(cls.regex, (
            [path('/', (sub_patterns, cls.app_name, cls.name))],
            cls.app_name,
            cls.name
        )))
        print(patterns)
        return patterns

    def urlinclude(cls, prefix=None):
        urlpatterns = [cls.urlpattern]
        for route in cls.routes:
            urlpatterns.append(route.urlpattern)
            if route.routes:
                urlpatterns.append(
                    path(route.regex, ([r.urlpattern for r in route.routes],cls.app_name, route.namespace))
                )
        return path(
            prefix or '',
            (
                urlpatterns,
                cls.app_name,
                cls.namespace,
            )
        )

    def urlresolver(cls):
        print(cls.regex, cls.namespace)
        return path(
            cls.regex,
            (
                [
                    path('', cls.as_view(), name=cls.name),
                ],
                cls.app_name,
                cls.namespace
            ),
        )
        return URLResolver(
            RegexPattern(prefix or ''),
            cls,
            app_name=cls.app_name,
            namespace=cls.namespace,
        )

    @property
    def urlobject(cls):
        if cls.routes:
            return cls.urlresolver()
        else:
            return cls.urlpattern


@six.add_metaclass(RouteMetaclass)
class Route(View):
    pass
