from __future__ import unicode_literals

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from .models import Media
from .models import Usuario
from .models import MediaSerializer
from .models import UsuarioSerializer
from django.shortcuts import render
from django.http import HttpResponse

from .forms import UsuarioForm


# Create your views here.
@csrf_exempt
def index(request):
    lista_media = Media.objects.all()
    return HttpResponse(serializers.serialize("json", lista_media))


@csrf_exempt
def detalle(request, media_id):
    lista_detalle = Media.objects.filter(id_media=str(media_id))
    return HttpResponse(serializers.serialize("json", lista_detalle))


def ver_media(request):
    return render(request, "polls/index.html")


def ver_detalle(request):
    return render(request, "polls/detalle_video.html")

def registrar_usuario(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form_data = form.cleaned_data
        nombre = form_data.get("nombre")
        apellido = form_data.get("apellido")
        foto = form_data.get("foto")
        pais = form_data.get("pais")
        ciudad = form_data.get("ciudad")
        email = form_data.get("email")
        username = form_data.get("username")
        password = form_data.get("password")

        obj = Usuario.objects.create(nombre=nombre, apellido = apellido, foto = foto, pais =pais,ciudad=ciudad,email=email,username=username,password=password)


    context = {
        "form": form,
    }
    return  render(request,"polls/registrar_usuario.html",context)