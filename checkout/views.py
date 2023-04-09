import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from order.models import Order, OrderItem, AnonymousUser
from order.forms import AnonymousOrderSearchForm
from store.models import Product
from accounts.models import Address
from basket.basket import Basket

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
            session['anonymous_user'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'phone_number': form.cleaned_data['phone_number'],
                'district_or_city': form.cleaned_data['district_or_city'],
                'street_address': form.cleaned_data['street_address'],
                'other_address': form.cleaned_data['other_address'],
                'additional_notes': form.cleaned_data['additional_notes'],
            }
            return redirect('checkout:payment_selection')
    else:
        if 'anonymous_user' in session:
            form = NoAuthCheckoutForm(
                initial={
                    'first_name': session['anonymous_user']['first_name'],
                    'last_name': session['anonymous_user']['last_name'],
                    'email': session['anonymous_user']['email'],
                    'phone_number': session['anonymous_user']['phone_number'],
                    'district_or_city': session['anonymous_user']['district_or_city'],
                    'street_address': session['anonymous_user']['street_address'],
                    'other_address': session['anonymous_user']['other_address'],
                    'additional_notes': session['anonymous_user']['additional_notes'],
                }
            )
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


def payment_selection(request):
    address = None
    if request.user.is_authenticated:
        address = Address.objects.filter(customer=request.user).order_by("-default")
        if "address" not in request.session:
            messages.success(request, "Please select address option")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        address = request.session['anonymous_user']

    return render(request, "checkout/payment.html", {"addresses": address})

#pay pal 



def payment_complete(request):
    session = request.session
    body = json.loads(request.body)
    basket = Basket(request)
    delivery_option = get_object_or_404(DeliveryOptions, pk=session["purchase"]["delivery_id"])

    if request.user.is_authenticated:
        user_id = request.user.id

        order = Order.objects.create(
            user_id=user_id,
            full_name=body['fullname'],
            email=body['email'],
            address1=body['address_1'],
            address2=body['address_2'],
            postal_code=body['postalCode'],
            country_code=body['countryCode'],
            total_paid=body['totalPaid'],
            order_key=body['orderId'],
            payment_option="paypal",
            delivery_option=delivery_option,
            billing_status=True,
        )
        order_id = order.pk
    else:
        if 'anonymous_user' in session:
            annony_user = AnonymousUser.objects.create(
                name = session['anonymous_user']['first_name']+' '+session['anonymous_user']['last_name'],
                email = session['anonymous_user']['email'],
                address1 = session['anonymous_user']['street_address'],
                address2 = session['anonymous_user']['other_address'],
                city = session['anonymous_user']['email'],
                phone = session['anonymous_user']['phone_number'],
            )
            annony_user_id = annony_user.id

        order = Order.objects.create(
            anony_user_id=annony_user_id,
            full_name=body['fullname'],
            email=body['email'],
            address1=body['address_1'],
            address2=body['address_2'],
            phone=session['anonymous_user']['phone_number'],
            postal_code=body['postalCode'],
            country_code=body['countryCode'],
            total_paid=body['totalPaid'],
            delivery_option=delivery_option,
            order_key=body['orderId'],
            payment_option="paypal",
            billing_status=True,
        )
        order_id = order.pk
        

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])
        product = get_object_or_404(Product, pk=item["product"].id)
        in_stock = product.in_stock
        new_stock = in_stock - item['qty']
        product.in_stock = new_stock
        product.save()

    return JsonResponse("Payment completed!", safe=False)



def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    if 'anonymous_user' in request.session:
        del request.session['anonymous_user']

    form = AnonymousOrderSearchForm()
    return render(request, "checkout/success.html", {'form': form})
