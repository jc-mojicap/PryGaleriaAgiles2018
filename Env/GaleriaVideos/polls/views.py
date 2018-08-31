from __future__ import unicode_literals
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Media, UserForm, EditUserForm
from .models import Usuario
from .models import Clip, ClipSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
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
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data.get("username")
            first_name = form_data.get("first_name")
            last_name = form_data.get("last_name")
            email = form_data.get("email")
            password = form_data.get("password")

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email

            user_app = Usuario(picture=form_data.get('picture'),
                               country=form_data.get('country'),
                               city=form_data.get('city'),
                               auth_user=user_model)
            user_model.save()
            user_app.save()
            return HttpResponseRedirect(reverse('media1:verMedia'))
    else:
        form = UserForm()

    context = {"form": form}
    return render(request, "polls/registrar_usuario.html", context)


def modificar_usuario(request):
    form = EditUserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form_data = form.cleaned_data
        first_name = form_data.get("first_name")
        last_name = form_data.get("last_name")
        picture = form_data.get("picture")
        country = form_data.get("country")
        city = form_data.get("city")
        email = form_data.get("email")
        username = form_data.get("username")
        password = form_data.get("password")

        obj = Usuario.objects.create(first_name=first_name, last_name=last_name, picture=picture, country=country,
                                     city=city, email=email, username=username, password=password)
    context = {
        "form": form,
    }
    return render(request, "polls/modificar_usuario.html", context)


def add_user_view(request):
    if request.method == 'POST' :
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            password = cleaned_data.get ('password')
            email = cleaned_data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()

            # return HttpResponseRedirect(reverse('media1:index'))
            return render(request, "polls/index.html")
    else:
        form = UserForm()
    context = {
        "form": form
    }
    return render(request, 'polls/Registro.html', context)


def login_view(request):

    if request.user.is_authenticated():
        # return redirect(reverse('media1:index'))
        return render(request, "polls/index.html")

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            # return redirect(reverse('media1:index'))
            return render(request, "polls/index.html")
        else:
            mensaje = 'Credenciales de acceso incorrectas'

    return render(request, 'polls/login.html', {'mensaje': mensaje})


def logout_view(request):
    logout(request)
    return render(request, "polls/index.html")


def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=form.user)
            return HttpResponseRedirect(reverse('media1:index'))
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'polls/updatePassword.html', context)
