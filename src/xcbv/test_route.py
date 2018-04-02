import re

from django.urls import reverse

from xcbv.shortcuts import *
from xcbv_examples.full.models import Person, Pet, Toy

import pytest


def test_simple_route():
    route = Route.factory(name='simple')
    assert len(route.urlpatterns()) == 1


def test_adding_sibbling():
    route = Route.factory(name='simple')
    assert len(route.urlpatterns()) == 1


'''
def test_named_route():
    route = Route.factory(name='lol')

    assert route.regex == 'lol'
    assert route.namespace == None
    assert route.app_name == None
    assert route.model == None
    assert reverse('lol', route) == '/lol'
    assert route.urlresolver().resolve('lol')
    assert len(route.urlresolver().url_patterns) == 1


def test_named_model_route():
    route = Route.factory(name='lol', model=Person)
    assert route.regex == 'lol'


def test_model_route_name():
    assert Route.factory(model=Person).name == 'person'


def test_app_name_inheritance():
    route = Route.factory(Route.factory(), app_name='lol')

    assert route.app_name == 'lol'
    assert route.routes[0].app_name == 'lol'


def test_model_route():
    route = Route.factory(model=Person)

    assert route.app_name == 'full'
    assert route.model == Person


def test_model_inheritance():
    assert 'full' == Person._meta.app_label  # prefligth

    route = Route.factory(
        Route.factory(name='friend'),
        model=Person
    )

    assert route.app_name == 'full'
    assert route.model == Person
    assert route.regex == 'person'
    assert route.routes[0].app_name == 'full'
    assert route.routes[0].model == Person
    assert route.routes[0].regex == 'friend'
    assert route.routes[0].name == 'friend'

    resolver = route.urlresolver()
    assert resolver.resolve('person').func.view_class.name == 'person'
    assert resolver.resolve('person/friend').func.view_class.name == 'friend'
    for i in ['p', 'person/fo', 'person/friend/', 'person/friend/foo']:
        with pytest.raises(Exception):
            resolver.resolve(i)

    assert reverse('person', route) == '/person'
    assert reverse('friend', route) == '/person/friend'


def test_nested_model_routes():
    route = Route.factory(
        Route.factory(
            Route.factory(
                model=Toy,
            ),
            model=Pet,
        ),
        model=Person
    )
    assert reverse('person', route) == '/person'
    assert reverse('pet:pet', route) == '/person/pet'
    assert reverse('pet:toy', route) == '/person/pet/toy'


def test_model_override():
    route = Route.factory(Route.factory(model=Pet), model=Person)

    assert route.model == Person
    assert route.routes[0].model == Pet


def test_route_regex():
    route = Route.factory(regex='bar')
    assert route.regex == 'bar'
    assert route.urlpattern.pattern.regex == re.compile('bar$')


def test_route_resolve():
    route = Route.factory(Route.factory(model=Pet), model=Person)
    resolver = route.urlresolver()
    assert resolver.resolve('person')
    assert resolver.resolve('person/pet')
    with pytest.raises(Exception):
        assert resolver.resolve('p')
    with pytest.raises(Exception):
        assert resolver.resolve('person/')
    with pytest.raises(Exception):
        assert resolver.resolve('person/pe')
    with pytest.raises(Exception):
        assert resolver.resolve('person/pet/a')


def test_full_example():
    assert reverse('person:list') == '/person/list'
    assert reverse('person:pet:list') == '/person/list'
'''
