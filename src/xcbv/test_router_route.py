from xcbv.shortcuts import *
from xcbv_examples.full.models import Person, Pet

import pytest


def test_route_model_from_router_model():
    assert Router(Route, model=Person).routes[0].model == Person


def test_router_route_integration():
    class ListView(Route):
        pass

    r = Router(
        ListView,
        Router(
            ListView,
            model=Pet,
        ),
        model=Person,
    )

    personlist = r.routes[0]
    assert personlist.name == 'list'
    assert personlist.path == 'list/'
    assert personlist.namespace == 'person'
    assert personlist.app_name == 'full'

    petlist = r.routes[1].routes[0]
    assert petlist.name == 'list'
    assert petlist.path == 'list/'
    assert petlist.namespace == 'pet'
    assert petlist.app_name == 'full'


def test_router_model_on_view_with_null_model():
    class ListView(Route):
        model = None

    r = Router(ListView, model=Person)
    assert r.routes[0].model == Person
