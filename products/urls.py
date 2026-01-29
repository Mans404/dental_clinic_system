from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('bulk-import/', views.product_bulk_import, name='product_bulk_import'),
    path('edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('autocomplete/', views.product_autocomplete, name='product_autocomplete'),
]
