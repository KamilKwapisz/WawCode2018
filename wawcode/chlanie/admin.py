from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .models import Uzytkownik, Lokal, Wlasciciel, WydarzenieUzytkownika, WydarzenieLokalu
urlpatterns = [
    path('', include('chlanie.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
admin.site.register(Uzytkownik)
admin.site.register(Lokal)
admin.site.register(Wlasciciel)
admin.site.register(WydarzenieLokalu)
admin.site.register(WydarzenieUzytkownika)
