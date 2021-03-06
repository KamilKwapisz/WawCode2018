from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .models import Lokal, Comment, Rate, Like

urlpatterns = [
    path('', include('chlanie.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.register(Lokal)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Like)
