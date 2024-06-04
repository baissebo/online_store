from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, products_list, products_details


app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('base/', products_list, name='products_list'),
    path('products/<int:pk>/', products_details, name='products_details')
]
