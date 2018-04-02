
from django.urls import path
from django.views.generic import View


app_name = 'c'
urlpatterns = [
    path('c', View.as_view(), name='lol')
]
