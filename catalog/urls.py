from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import HomeView, ContactsView, ProductListView, ProductDetailView, ProductCreateView, \
    BlogPostCreateView, BlogPostUpdateView, BlogPostListView, BlogPostDetailView, BlogPostDeleteView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('base/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('create-product/', ProductCreateView.as_view(), name='product_create'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product-delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('create-post/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('post-update/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('post-list/', BlogPostListView.as_view(), name='blogpost_list'),
    path('post-detail/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('post-delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
