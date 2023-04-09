from . import views
from django.urls import path


app_name = "store"

urlpatterns = [
    #store urls
    path('', views.home, name='home'),
    path('product-detail/<uuid:product_url>/', views.product_detail, name='product-detail'),
    path('shop/', views.shopView, name='shop'),
    path('category/<slug:category_slug>/', views.product_category, name='category-list'),
    path('search/', views.searchView, name='search'),

    #blog urls
    path('blog-list/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('blog/filter=/<slug:blog_slug>', views.BlogListCategoryView.as_view(), name='blog-category-list'),

    #contact
    path('contact/', views.contactView, name='contact'),
]