# flake8: noqa: D101
from xcbv_examples.full.views import PersonIndex
from django.urls import path

urlpatterns = [
    path('person/', (PersonIndex.urlpatterns(), PersonIndex.app_name, PersonIndex.namespace))
]

'''
urlpatterns = [
    path('person', PersonIndex.as_view(), name='person'),
    path('person/', (
        [r.urlpattern for r in PersonIndex.routes],
        'full',
        'person',
    )),
]
'''


from xcbv.shortcuts import Route
from xcbv_examples.full.models import *
route = Route.factory(
        Route.factory(
            Route.factory(
                model=Toy,
            ),
            model=Pet,
        ),
        model=Person
    )
#urlpatterns += [route.factory(namespace='test', regex='lol').]

'''
from django.urls import path, include
from django.contrib import admin
urlpatterns += [path('admin/', admin.site.urls)]


from django.conf import settings
from django.conf.urls import include, url

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

'''
