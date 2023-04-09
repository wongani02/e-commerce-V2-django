from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.db.models import Q

from basket.basket import Basket

from .models import Order, OrderItem
from .forms import AnonymousOrderSearchForm


def getOrder(request):
    # q = None
    form = AnonymousOrderSearchForm()
    if request.method == 'POST':
        form = AnonymousOrderSearchForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['order_email']
            order_key = form.cleaned_data['order_key']
            try:
                order = get_list_or_404(Order, email=email, order_key=order_key)
            except:
                context = {'form':form,}
                return render(request, 'order/order-not-found.html', context)     
    context = {
        'order': order,
    }
    return render(request, 'order/my-account.html', context)


def orderTrackingView(request):
    form = AnonymousOrderSearchForm()
    if request.method == 'POST':
        form = AnonymousOrderSearchForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['order_email']
            order_key = form.cleaned_data['order_key']
            try:
                order = get_list_or_404(Order, email=email, order_key=order_key)
                return render(request, 'order/my-account.html', context={'order': order,})
            except:
                context = {'form':form,}
                return render(request, 'order/order-not-found.html', context)     
    context = {
        'form':form,
    }
    return render(request, 'order/order-tracking.html', context)

