from django.urls import path
from . import views

app_name = 'chlanie'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
]