from xcbv.shortcuts import *

import pytest


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


def test_router_with_namespace_as_classattr():
    class Test(Router):
        namespace = 'b'

    r = Test(Test)
    assert r.namespace == 'b'
    assert r.children[0].namespace == 'b'

    r = Test(Test, namespace='a')
    assert r.namespace == 'a'
    assert r.children[0].namespace == 'b'

    r = Test(Test(namespace='a'))
    assert r.namespace == 'b'
    assert r.children[0].namespace == 'a'


def test_router_namespace_clash():
    r = Router(namespace='a')
    with pytest.raises(NamespaceCollision):
        r = Router(r, r, namespace='a')


def test_router_with_app_name():
    r = Router(app_name='a')
    assert r.namespace == 'a'
    assert r.app_name == 'a'


def test_router_route_app_name():
    r = Router(Route, app_name='a')
    assert r.children[0].namespace == 'a'
    assert r.children[0].app_name == 'a'
