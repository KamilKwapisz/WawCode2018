from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'chlanie'

urlpatterns = [
    path('', views.index, name='index'),
    path('lokal/dodaj/', views.LokalCreateView.as_view(), name='lokal-create'),
    path('lokal/<int:pk>', views.lokal_detail_view, name='lokal-detail'),
    path('search/', views.search_test, name='search'),
    path('ulubione/', views.ulubione, name='ulubione'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('ajax/lokale', views.get_lokals_list, name='lokale'),
    path('ajax/rating', views.rate, name='rating'),
    path('ajax/comment', views.comment, name='comment'),
    path('ajax/reservation', views.reservation, name='reservation'),
    path('ajax/favourite', views.favourite, name='favourite'),
]