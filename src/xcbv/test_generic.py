from xcbv.generic import *

from xcbv_examples.full.models import Person


'''

def test_detailview():
    view = DetailView.factory(model=Person)
    assert view.regex == '(?P<pk>[^/]+)'
    view = view.factory(pk_url_kwarg='person_pk')
    assert view.regex == '(?P<person_pk>[^/]+)'


def test_createview():
    assert CreateView.factory(model=Person).urlpattern


def test_updateview():
    assert UpdateView.factory(model=Person).urlpattern


def test_listview():
    assert ListView.factory(model=Person).urlpattern


def test_deleteview():
    assert DeleteView.factory(model=Person).urlpattern
'''
