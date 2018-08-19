from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^media/$', views.index, name='index'),
    url(r'^ver_media/$', views.ver_media, name='verMedia'),
]