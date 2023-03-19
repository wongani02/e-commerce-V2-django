from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

from .models import *


# Create your views here.



def home(request):
    # products = Product.objects.all()
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    context = {
        'products': products,
        'active': 'active'
    }
    return render(request, 'store/home.html', context)


def categories(request):

    ''' 
    This view is accesible from all pages because it is
    added to the context manager in the settings.py file
    '''

    return {'category': Category.objects.filter(level=0),}


def product_detail(request, product_url):

    '''
    Single product view
    '''

    product = get_object_or_404(Product, product_url=product_url, is_active=True)
    context = {
        'product': product,
    }
    return render(request, 'store/product-details-affiliate.html', context)


def product_category(request, category_slug):
    '''
    View to filter products by category
    consists of mptt queries
    '''
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
        )
    context = {
        'products': products,
        'category_name': category,
    }
    return render(request, 'store/shop-no-sidebar.html', context)


def shopView(request):
    products = Product.objects.filter(is_active=True)
    context = {
        'products': products,
        'name': 'Shop',
        'active_s': 'active'
    }
    return render(request, 'store/shop.html', context)


def searchView(request):
    if request.method == 'POST':
        param = request.POST['search_q']
        
        if param == '':
            messages.info(request, 'Please enter search parameters')
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        products = Product.objects.filter(
            Q(category__in=Category.objects.filter(name__icontains=param).get_descendants(include_self=True))|Q(product_name__icontains=param)|Q(description__icontains=param)
        ).distinct()
        print(products)
    context = {
        'products': products,
        'name': 'Search results for \'{}\''.format(param)
    }
    return render(request, 'store/shop.html', context)

