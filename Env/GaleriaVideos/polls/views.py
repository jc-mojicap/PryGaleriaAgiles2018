from __future__ import unicode_literals
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Media, UserForm, EditUserForm, CategoriaSerializer, Categoria, EditUsuarioForm
from .models import Usuario
from .models import Clip, ClipSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request, HttpResponseBadRequest
from django.core.mail import send_mail
import json
from datetime import datetime
from django.core import serializers as jsonserializer

# API
@csrf_exempt
def index(request):
    lista_media = Media.objects.all()
    if request.method == 'POST':
        jsonFilter = json.loads(request.body)
        fcategoria = jsonFilter['categoria']
        ftipo = jsonFilter['tipo']
        categoria = Categoria.objects.filter(nombre=fcategoria)
        lista_media = Media.objects.filter(categoria=categoria, tipo=ftipo)
    return HttpResponse(serializers.serialize("json", lista_media))

@csrf_exempt
def categoria(request):
    lista_categoria = Categoria.objects.all()
    return HttpResponse(serializers.serialize("json", lista_categoria))


@csrf_exempt
def detalle(request, media_id):
    lista_detalle = Media.objects.filter(id_media=str(media_id))
    return HttpResponse(serializers.serialize("json", lista_detalle))

@csrf_exempt
def detalle_clips(request, media_id):
    lista_clips = Clip.objects.filter(media=media_id)
    serializer = ClipSerializer(lista_clips, many=True)
    return HttpResponse(json.dumps(serializer.data), content_type='application/json')

@csrf_exempt
def create_clip(request, media_id):
    if request.method == "POST":
        clip = json.loads(request.body)
        seg_ini = clip.get("seg_ini")
        seg_fin = clip.get("seg_fin")
        new_clip = Clip(
            nombre=clip.get("nombre"),
            seg_ini=datetime.strptime(seg_ini,"%H:%M:%S").time(),
            seg_fin=datetime.strptime(seg_fin,"%H:%M:%S").time(),
            usuario=User.objects.get(username=request.user),
            media=Media.objects.get(pk=media_id)
        )
        new_clip.save()
        enviar_email(media_id)
        return HttpResponse(serializers.serialize("json", [new_clip]))

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
    if request.method == 'POST':
        form = EditUserForm(data=request.POST, instance=request.user)
        user = User.objects.get(username=request.user.username)
        usuario = Usuario.objects.filter(auth_user=user).first()
        usuarioform = EditUsuarioForm(request.POST, request.FILES, instance=usuario)
        passform = PasswordChangeForm(data=request.POST, user=request.user)

        if passform.is_valid():
            passform.save()
            update_session_auth_hash(request, user=form.user)
            return HttpResponseRedirect(reverse('media1:index'))

        elif form.is_valid():
            if usuarioform.is_valid():
                form.save()
                usuarioform.save()
                return HttpResponseRedirect(reverse('media1:verMedia'))
    else:
        user = User.objects.get(username=request.user.username)
        form = EditUserForm(instance=user)
        usuario = Usuario.objects.filter(auth_user=user).first()
        usuarioform = EditUsuarioForm(instance=usuario)
        passform = PasswordChangeForm(user=request.user)

    context = {
        "form": form,
        "usuarioform": usuarioform,
        "passform":passform
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


def enviar_email(media_id):
    media = Media.objects.get(pk=media_id)
    send_mail(
        'Clip agregado',
        'Se ha agregado un clip a: ' + media.titulo,
        'sw.jmojica@gmail.com',
        [media.user.email],
        fail_silently=False,
    )
