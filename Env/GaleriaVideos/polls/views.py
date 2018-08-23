from __future__ import unicode_literals

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from .models import Media, MediaForm
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
@csrf_exempt
def index(request):
    lista_media = Media.objects.all()
    return HttpResponse(serializers.serialize("json", lista_media))


def ver_media(request):
    return render(request, "polls/index.html")


