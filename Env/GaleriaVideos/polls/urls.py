from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.ver_media, name='index'),
    url(r'^media/$', views.index, name='index'),
    url(r'^ver_media/$', views.ver_media, name='verMedia'),
    url(r'^ver_detalle/$', views.ver_detalle, name='verDetalle'),
    url(r'^detalle/(?P<media_id>[0-9]+)/$', views.detalle, name='detalle'),
    url(r'^detalle/(?P<media_id>[0-9]+)/clips/$', views.detalle_clips, name='detalleClips'),
    url(r'^registrar_usuario/$', views.registrar_usuario, name="registrarUsuario"),
    url(r'^modificar_usuario/$', views.modificar_usuario, name="modificarUsuario"),
    url(r'^update_password/$', views.update_password, name="updatePassword"),
    url(r'^addUser/$', views.add_user_view, name='addUser'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
