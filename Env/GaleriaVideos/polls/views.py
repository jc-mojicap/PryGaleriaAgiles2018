from __future__ import unicode_literals

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from .models import Media
from .models import Usuario
from .models import MediaSerializer
from .models import UsuarioSerializer
from django.shortcuts import render
from django.http import HttpResponse


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