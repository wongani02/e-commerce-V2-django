from . import views
from django.urls import path

app_name = "checkout"

urlpatterns = [
    path('delivery-choices/', views.delivery_choices, name='delivery-choices'),
    path("basket_update_delivery/", views.basket_update_delivery, name="basket_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"), 
    path("auth-handler/", views.checkout_handler, name='auth-handler'),
    path("address/checkout/", views.noAuthCheckoutView, name='no-auth-checkout'),
    #payment 
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),

]