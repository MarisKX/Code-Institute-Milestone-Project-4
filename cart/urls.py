from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('add_to_cart/<item_id>/', views.add_to_cart, name='add_to_cart'),
]
