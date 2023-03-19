import json

from accounts.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from order.models import Order, OrderItem
from store.models import Product

from .models import DeliveryOptions
from .forms import NoAuthCheckoutForm

# Create your views here.

'''
View to output the delivery options
'''
@login_required
def delivery_choices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    context = {
        "deliveryoptions": deliveryoptions,
    }

    return render(request, "checkout/delivery_choices.html", context)


''' 
This function will fire once a delivery option has been selected 
via AJAX which is implemeted in the cart.html template,
It will then modify the session and add the delivery price to the 
session and return a JSON response to the frontend.
'''
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)
        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True
        response = JsonResponse({"total": str(updated_total_price), "delivery_price": str(delivery_type.delivery_price)})
        return response
    

def checkout_handler(request):
    if request.user.is_authenticated:
        return redirect('checkout:delivery_address')
    else:
        return redirect('checkout:no-auth-checkout')


def noAuthCheckoutView(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    if request.method == "POST":
        form = NoAuthCheckoutForm(request.POST) 
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = NoAuthCheckoutForm()
    context = {
        'form': form,
    }
    return render(request, 'checkout/no-auth-checkout.html', context)


@login_required(redirect_field_name='checkout:delivery_address', login_url='accounts:accounts-login')
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    if not addresses:
        messages.success(request, "Please add an address before you checkout")
        return redirect('accounts:add_address')

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True
    
    context = {"addresses": addresses}

    return render(request, "checkout/checkout.html", context)


# def check_page(request):
#     addresses = Address.objects.filter(customer=request.user).order_by("-default")
#     return render(request, 'checkout/checkout.html', {'addresses': addresses})

@login_required
def payment_selection(request):
    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment.html", {"addresses": addresses})

#pay pal 

from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])
        product = get_object_or_404(Product, pk=item["product"].id)
        print(product)
        in_stock = product.in_stock
        new_stock = in_stock - item['qty']
        product.in_stock = new_stock
        product.save()

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/success.html", {})
