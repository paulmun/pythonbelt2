from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^dashboard$', views.index, name='wishlist_index'),
	url(r'^wish_items/new$', views.new, name='wishlist_new'),
	url(r'^wish_items/create$', views.create, name='wishlist_create'),
	url(r'^wish_items/add/(?P<itemID>[0-9]+$)', views.add, name='wishlist_add'),
	url(r'^wish_items/(?P<itemID>[0-9]+$)', views.show, name='wishlist_show'),
	url(r'^wish_items/remove/(?P<itemID>[0-9]+$)', views.remove, name='wishlist_remove')
]
