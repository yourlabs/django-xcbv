from .exceptions import *
from .route import Route


class Router(object):
    parent = None
    children = []

    def __init__(self, *children, **state):
        for key, value in state.items():
            setattr(self, key, value)

        self.namespace_init()
        self.children_init(children)

    def namespace_init(self):
        namespace = getattr(self, 'namespace', None)
        if not namespace:
            app_name = getattr(self, 'app_name', None)
            if app_name:
                self.namespace = app_name
            else:
                raise RouterNamespaceNotResolvable()

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
