from __future__ import unicode_literals
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Clip, Media, ClipSerializer
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UsuarioForm
import json


# API
@csrf_exempt
def index(request):
    lista_media = Media.objects.all()
    return HttpResponse(serializers.serialize("json", lista_media))


@csrf_exempt
def detalle(request, media_id):
    lista_detalle = Media.objects.filter(id_media=str(media_id))
    return HttpResponse(serializers.serialize("json", lista_detalle))

@csrf_exempt
def detalle_clips(request, media_id):
    lista_clips = Clip.objects.filter(media=media_id)
    serializer = ClipSerializer(lista_clips, many=True)
    return HttpResponse(json.dumps(serializer.data), content_type='application/json')


# Views
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
    return render(request,"polls/registrar_usuario.html",context)