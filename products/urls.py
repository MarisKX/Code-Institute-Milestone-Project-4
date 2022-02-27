from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:ean_code>/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:ean_code>/', views.update_product, name='update_product'),
    path('delete_product/<int:ean_code>/', views.delete_product, name='delete_product'),
]
