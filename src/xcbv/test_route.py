from xcbv.shortcuts import *
from xcbv_examples.full.models import Person, Pet

import pytest


class PersonListView(Route):
    pass


def test_route_path():
    with pytest.raises(RoutePathNotResolvable):
        Route.path

    assert Route.factory(path='lol/').path == 'lol/'


def test_route_path_from_name():
    assert Route.factory(name='lol').path == 'lol/'


def test_route_name_from_class_name():
    assert PersonListView.name == 'personlist'


def test_route_with_model():
    v = PersonListView.factory(model=Person)
    assert v.name == 'list'
    assert v.path == 'list/'
    assert v.namespace == 'person'
    assert v.app_name == 'full'


def test_with_model_none():
    class ListView(Route):
        model = None

    assert ListView.factory(model=Person).model == Person


def test_route_nesting():
    r = Route.factory(Route, model=Person)
    assert r.model == Person
