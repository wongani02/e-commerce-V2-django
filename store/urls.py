from . import views
from django.urls import path

app_name = "store"

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<uuid:product_url>/', views.product_detail, name='product-detail'),
    path('shop/', views.shopView, name='shop'),
    path('category/<slug:category_slug>/', views.product_category, name='category-list'),
    path('search/', views.searchView, name='search'),
]