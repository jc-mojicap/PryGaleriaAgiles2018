from django.db import models
from rest_framework import serializers
from django.forms import ModelForm

# Create your models here.


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)
    apellido = models.CharField(max_length=30, blank=True)
    foto = models.CharField(max_length=1000,blank=True)
    pais = models.CharField(max_length=30, blank=True)
    ciudad = models.CharField(max_length=30,blank=True)
    email = models.CharField(max_length=204, blank=True)
    username = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Media(models.Model):
    id_media = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000)
    titulo = models.CharField(max_length=150, blank=True)
    autor = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateField()
    ciudad = models.CharField(max_length=30, blank=True)
    pais = models.CharField(max_length=30, blank=True)
    id_categoria = models.ForeignKey(Categoria, null=True)
    id_tipo = models.ForeignKey(Tipo, null=True)
    id_usuario = models.ForeignKey(Usuario, null=True)

    def __unicode__(self):
        return self.titulo


class Clip(models.Model):
    id_nombre_clip = models.AutoField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)
    seg_ini = models.TimeField()
    seg_fin = models.TimeField()
    id_usuario = models.ForeignKey(Usuario, null=True)

    def __unicode__(self):
        return self.nombre


class Favorito(models.Model):
    id_categoria = models.ForeignKey(Categoria, null=True)
    id_usuario = models.ForeignKey(Usuario, null=True)

    def __unicode__(self):
        return self.id_categoria


class TipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tipo
        fields = ('nombre')


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ('nombre')


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'foto', 'pais', 'ciudad', 'email', 'username')


class MediaSerializer(serializers.ModelSerializer):
    owner = UsuarioSerializer(read_only=True)
    ownerId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Usuario.objects.all(), source='usuario')
    tipo = TipoSerializer(read_only=True, source='tipo')
    categoria = TipoSerializer(read_only=True, source='categoria')

    class Meta:
        model = Media
        fields = ('url', 'titulo', 'autor', 'fecha_creacion', 'ciudad', 'pais', 'categoria', 'tipo', 'usuario')
