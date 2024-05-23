from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('historical-data/', views.historical_data_view, name='historical_data_view'),
    path('historical_data_json/', views.historical_data_json, name='historical_data_json'),
]
