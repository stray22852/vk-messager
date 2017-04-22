from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^get/$', views.get_dialogs, name='get_dialogs'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^get/dialog/(?P<us_id>[0-9]+)$', views.dialog, name='dialog'),
    url(r'^get/dialog/(?P<fr_id>[0-9]+)/photo$', views.get_foto, name='get_foto'),
    url(r'^set-status/$', views.set_status, name='set_status'),
    url(r'^spocess/$', views.sprocess, name='sprocess'),
]
