from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.reroute, name='logreg_init'),
    url(r'^main$', views.index, name='logreg_index'),
    url(r'^register$', views.register, name='logreg_register'),
    url(r'^login$', views.login, name='logreg_login'),
    url(r'^logout$', views.logout, name='logreg_logout')
]
