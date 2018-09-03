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


class Tipo(models.Model):
    tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Usuario(models.Model):
    picture = models.ImageField(upload_to="images", blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    auth_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __unicode__(self):
        return self.auth_user.username


class Media(models.Model):
    id_media = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000)
    titulo = models.CharField(max_length=150, blank=True)
    autor = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateField()
    ciudad = models.CharField(max_length=30, blank=True)
    pais = models.CharField(max_length=30, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT,null=True)
    tipo = models.CharField(max_length=30, blank=True)
    # tipo = models.ForeignKey(Tipo,on_delete=models.PROTECT,null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    # usuario = models.ForeignKey(Usuario, null=True)

    def __unicode__(self):
        return self.titulo


class Clip(models.Model):
    id_nombre_clip = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)
    seg_ini = models.TimeField()
    seg_fin = models.TimeField()
    usuario = models.ForeignKey(User, null=True)
    media = models.ForeignKey(Media, null=True)

    def __unicode__(self):
        return self.nombre


class Favorito(models.Model):
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT,null=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT,null=True)

    def __unicode__(self):
        return self.id_categoria


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ('nombre')

class TipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tipo
        depth = 1
        fields = "__all__"


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
#         model = pictures
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
            raise forms.ValidationError('Las Claves no coinciden.')
        return password2


class EditUsuarioForm(ModelForm):
    picture = models.ImageField(upload_to="images", blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    auth_user = models.ForeignKey(User, null=False)

    class Meta:
        model = Usuario
        fields = ('picture', 'country', 'city')


class EditUserForm(ModelForm):
    username = forms.CharField(max_length=50, disabled=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario no existe.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la Base de Datos"""
        username = self.cleaned_data["username"]
        email1 = self.cleaned_data["email"]
        users = User.objects.filter(email__iexact=email1).exclude(username__iexact=username)
        if users:
            raise forms.ValidationError('E-mail regitrado por otro usuario')
        return email1.lower()