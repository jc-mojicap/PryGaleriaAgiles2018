from __future__ import unicode_literals
from .models import Media
from .models import Categoria
from .models import Clip
from .models import Usuario
from .models import Favorito
from django.contrib import admin

# Register your models here.
admin.site.register(Media)
admin.site.register(Categoria)
admin.site.register(Clip)
admin.site.register(Usuario)
admin.site.register(Favorito)
