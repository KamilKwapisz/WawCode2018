from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'chlanie'

urlpatterns = [
    path('', views.index, name='index'),
    path('lokal/dodaj', views.LokalCreateView.as_view(), name='lokal-create'),
    path('lokal/<int:pk>', views.LokalDetailView.as_view(), name='lokal-detail'),
    path('test/', views.sample_query, name='test'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]