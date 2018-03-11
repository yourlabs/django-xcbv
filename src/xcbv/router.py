from .exceptions import *
from .route import Route


class Router(object):
    parent = None
    routes = []

    def __init__(self, *routes, **state):
        for key, value in state.items():
            setattr(self, key, value)

        # Ensure namespace resolves or crash
        self.namespace
        self.routes_init(routes)

    def __getattr__(self, attr):
        if attr == 'namespace':
            return self.get_namespace()
        if attr == 'app_name':
            return self.get_app_name()
        if attr == 'path':
            return self.get_path()
        if attr == 'model':
            if self.parent:
                return self.parent.model
            return None
        return object.__getattribute__(self, attr)

    def get_path(self):
        model = getattr(self, 'model', None)
        if model:
            return model._meta.model_name + '/'
        return ''

    def get_namespace(self):
        app_name = getattr(self, 'app_name', None)
        model = getattr(self, 'model', None)
        if model:
            return model._meta.model_name
        elif app_name:
            return app_name
        else:
            raise RouterNamespaceNotResolvable()

    def get_app_name(self):
        if self.parent:
            return self.parent.app_name
        else:
            model = getattr(self, 'model', None)
            if model:
                return model._meta.app_label

    def routes_init(self, routes):
        routes = list(self.routes) + list(routes)
        self.routes = []
        for route in routes:
            if isinstance(route, type):
                if issubclass(route, Route):
                    self.routes.append(route.factory(parent=self))
                elif issubclass(route, Router):
                    self.routes.append(route(parent=self))
            elif isinstance(route, Router):
                route.parent = self
                self.routes.append(route)

        namespaces = []
        for route in self.routes:
            if not isinstance(route, Router):
                continue
            if route.namespace in namespaces:
                raise NamespaceCollision()
            namespaces.append(route.namespace)
