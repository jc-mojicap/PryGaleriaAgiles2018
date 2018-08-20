from django.db import models
from django.forms import ModelForm

# Create your models here.


class Categoria(models.Model):
    id_categoria = models.IntegerField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Tipo(models.Model):
    id_tipo = models.IntegerField(auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.nombre


class Media(models.Model):
    url = models.CharField(max_length=1000)
    titulo = models.CharField(max_length=150, blank=True)
    autor = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateField()
    ciudad = models.CharField(max_length=30, blank=True)
    pais = models.CharField(max_length=30, blank=True)
    id_categoria = models.ForeignKey(Categoria, null=True)
    id_tipo = models.ForeignKey(Tipo, null=True)

    def __unicode__(self):
        return self.titulo


class MediaForm(ModelForm):

    class Meta:
        model = Media
        fields = ['url', 'titulo', 'autor', 'fecha_creacion', 'ciudad', 'pais']
