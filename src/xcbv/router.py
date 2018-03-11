from .exceptions import *
from .route import Route


class Router(object):
    parent = None
    children = []

    def __init__(self, *children, **state):
        for key, value in state.items():
            setattr(self, key, value)

        # Ensure namespace resolves or crash
        self.namespace
        self.children_init(children)

    def __getattr__(self, attr):
        if attr == 'namespace':
            return self.get_namespace()
        if attr == 'app_name':
            return self.get_app_name()
        if attr == 'path':
            return self.get_path()
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

    def children_init(self, children):
        children = list(self.children) + list(children)
        self.children = []
        for child in children:
            if isinstance(child, type):
                if issubclass(child, Route):
                    self.children.append(child.factory(parent=self))
                elif issubclass(child, Router):
                    self.children.append(child(parent=self))
            elif isinstance(child, Router):
                child.parent = self
                self.children.append(child)

        namespaces = []
        for child in self.children:
            if not isinstance(child, Router):
                continue
            if child.namespace in namespaces:
                raise NamespaceCollision()
            namespaces.append(child.namespace)
