from __future__ import unicode_literals
from .models import Media
from .models import Categoria
from .models import Tipo
from django.contrib import admin

# Register your models here.
admin.site.register(Media)
admin.site.register(Categoria)
admin.site.register(Tipo)