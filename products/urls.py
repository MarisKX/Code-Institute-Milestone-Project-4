from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<ean_code>/', views.product_details, name='product_details')
]