from django.urls import path
from . import views
app_name = 'product_packages'  # Uygulama adı tanımlandı
urlpatterns = [

    path("product_detail/<int:product_detail_pk>/", views.product_detail, name="product_detail"),

]
