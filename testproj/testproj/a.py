from django.urls import path, include
from django.views import generic


app_name = 'a'
urlpatterns = [
    path('b/', generic.TemplateView.as_view(template_name='a'), name='b'),
    path('b/', include('testproj.b', namespace='b'))
]
