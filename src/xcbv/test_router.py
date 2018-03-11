from xcbv.shortcuts import *
from xcbv_examples.full.models import Person, Pet

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


def test_router_path_empty():
    r = Router(namespace='full')
    assert r.path == ''


def test_router_path_specified():
    r = Router(path='lol/', namespace='full')
    assert r.path == 'lol/'


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


def test_router_gets_app_name_and_namespace_from_model():
    r = Router(model=Person)
    # would be resolvable both with app_name and namespace
    assert r.app_name == 'full'
    assert r.namespace == 'person'


def test_nested_model_router():
    r = Router(Router(model=Pet), model=Person)
    assert r.app_name == 'full'
    assert r.namespace == 'person'
    assert r.children[0].app_name == 'full'
    assert r.children[0].namespace == 'pet'


def test_nested_wraper_router_overriding_app_name():
    r = Router(Router(Router(model=Pet), model=Person), app_name='lol')
    assert r.app_name == 'lol'
    assert r.namespace == 'lol'
    assert r.children[0].app_name == 'lol'
    assert r.children[0].namespace == 'person'
    assert r.children[0].children[0].app_name == 'lol'
    assert r.children[0].children[0].namespace == 'pet'


def test_router_model_path():
    r = Router(model=Person)
    assert r.path == 'person/'

    r = Router(model=Person, path='')
    assert r.path == ''


def test_model_router_route_path():
    r = Router(Router(model=Pet), model=Person)
    assert r.path == 'person/'
    assert r.children[0].path == 'pet/'
