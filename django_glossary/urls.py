from django.conf.urls import url
from django.urls import path
from .views import TermDetailView, TermListView


app_name = 'django_glossary'
urlpatterns = [
    #url(r'^$', TermListView.as_view(), name='term-list'),
    path('', TermListView.as_view(), name='term-list'),
    url(r'^(?P<slug>[-\w]+)/$', TermDetailView.as_view(), name='term-detail'),
]
