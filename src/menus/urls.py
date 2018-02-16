from django.conf.urls import url
from .views import (
	ItemDetailView,
	ItemCreateView,
	ItemListView,
	ItemUpdateView
)

urlpatterns = [
	url(r'^$', ItemListView.as_view(), name='list'),
    url(r'^create/$', ItemCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/edit/$', ItemUpdateView.as_view(), name='edit'),
]
