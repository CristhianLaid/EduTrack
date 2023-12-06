from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Apps.Usuario import urls as usuario_urls
from Apps.Registro_academico.Datos_institucionales import urls as Datos_institucionales

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(usuario_urls)),
    path('course/', include(Datos_institucionales)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
