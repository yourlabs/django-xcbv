from django.urls import path, include
from django.views.generic import View


app_name = 'b'
urlpatterns = [path('c/', include('testproj.c', namespace='c'))]
