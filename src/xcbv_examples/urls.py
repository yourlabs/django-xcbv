# flake8: noqa: D101
from xcbv_examples.full.views import router

urlpatterns = [router.urlpattern]

'''
from django.urls import path, include
urlpatterns = [
    path('', include('xcbv.a', namespace='a'))
]
'''
