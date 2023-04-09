from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('get-order/', views.getOrder, name='get-order'),
    path('track-order/', views.orderTrackingView, name='track-order'),
]