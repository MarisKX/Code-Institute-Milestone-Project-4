from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('add_to_cart/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<item_id>/', views.update_cart, name='update_cart'),
    path('remove/<item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
