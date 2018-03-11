import pytest


class RouterNamespaceNotResolvable(Exception):
    pass


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
        return object.__getattr__(cls, attr)


class Route(metaclass=RouteMetaclass):
    pass


class Router(object):
    parent = None
    children = []

    def __init__(self, *children, **state):
        for key, value in state.items():
            setattr(self, key, value)

        namespace = getattr(self, 'namespace', None)
        if not namespace:
            app_name = getattr(self, 'app_name', None)
            if app_name:
                self.namespace = app_name
            else:
                raise RouterNamespaceNotResolvable()

        children = list(self.children) + list(children)
        self.children = []
        for child in children:
            if isinstance(child, type):
                if issubclass(child, Route):
                    self.children.append(child.factory(parent=self))
                elif issubclass(child, Router):
                    self.children.append(Router(parent=self))
            elif isinstance(child, Router):
                child.parent = self
                self.children.append(child)


def test_router_init():
    with pytest.raises(RouterNamespaceNotResolvable):
        Router()

    with pytest.raises(RouterNamespaceNotResolvable):
        Router(Router, namespace='a')

    with pytest.raises(RouterNamespaceNotResolvable):
        Router(Router(), namespace='a')


def test_router_namespace():
    r = Router(namespace='full')
    assert r.namespace == 'full'


def test_route_inherits_namespace():
    r = Router(Route, namespace='full')
    assert r.children[0].namespace == 'full'


def test_router_requires_namespace():
    with pytest.raises(RouterNamespaceNotResolvable):
        Router()


def test_router_override_parent_namespace():
    r = Router(Router(namespace='b'), namespace='a')
    assert r.namespace == 'a'
    assert r.children[0].namespace == 'b'


def test_router_with_app_name():
    r = Router(app_name='a')
    assert r.namespace == 'a'
    assert r.app_name == 'a'


def test_router_route_app_name():
    r = Router(Route, app_name='a')
    assert r.children[0].namespace == 'a'
    assert r.children[0].app_name == 'a'
