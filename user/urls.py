from django.urls import path
from . import views
app_name = 'user'  # Uygulama adı tanımlandı
urlpatterns = [
    path('profil/', views.profil, name='profil'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('user_logout/', views.user_logout, name='user_logout'),

]

