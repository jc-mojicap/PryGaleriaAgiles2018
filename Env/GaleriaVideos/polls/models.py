import email

from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from rest_framework import serializers
# from django import forms


# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Usuario(models.Model):
    picture = models.ImageField(upload_to="images")
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    auth_user = models.ForeignKey(User, null=False)

    def __unicode__(self):
        return self.name


class Media(models.Model):
    id_media = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000)
    titulo = models.CharField(max_length=150, blank=True)
    autor = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateField()
    ciudad = models.CharField(max_length=30, blank=True)
    pais = models.CharField(max_length=30, blank=True)
    categoria = models.ForeignKey(Categoria, null=True)
    tipo = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(User,null=True)
    # usuario = models.ForeignKey(Usuario, null=True)

    def __unicode__(self):
        return self.titulo


class Clip(models.Model):
    id_nombre_clip = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)
    seg_ini = models.TimeField()
    seg_fin = models.TimeField()
    usuario = models.ForeignKey(Usuario, null=True)
    media = models.ForeignKey(Media, null=True)

    def __unicode__(self):
        return self.nombre


class Favorito(models.Model):
    id_categoria = models.ForeignKey(Categoria, null=True)
    id_usuario = models.ForeignKey(Usuario, null=True)

    def __unicode__(self):
        return self.id_categoria


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ('nombre')


# class UsuarioSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Usuario
#         fields = ('nombre', 'apellido', 'foto', 'pais', 'ciudad', 'email', 'username')


# class MediaSerializer(serializers.ModelSerializer):
#     owner = UsuarioSerializer(read_only=True)
#     ownerId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Usuario.objects.all(), source='usuario')
#
#     class Meta:
#         model = Media
#         fields = ('url', 'titulo', 'autor', 'fecha_creacion', 'ciudad', 'pais', 'tipo', 'usuario')


class ClipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clip
        depth = 1
        fields = "__all__"


class UserForm(ModelForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('picture', 'country', 'city')

    def clean_username(self):
        """Comprueba que no exista un username igual en la Base de Datos"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la Base de Datos"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registado.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 segan iguales"""
        password=self.cleaned_data['password']
        password2=self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError ('Las Claves no coinciden.')
        return password2


class EditUserForm(ModelForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'picture', 'country', 'city')

    def clean_email(self):
        """Comprueba que no exista un email igual en la Base de Datos"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registado.')
        return email

