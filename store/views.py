from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import View, ListView
from django.core.mail import EmailMessage
from django.conf import settings

from hitcount.views import HitCountDetailView

from .models import *
from .forms import ContactForm


# Create your views here.


def home(request):
    # products = Product.objects.all()
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    blogs = BlogPost.objects.filter(is_active=True)[:3]
    featured = products.filter(is_featured=True)
    context = {
        'products': products,
        'blogs': blogs,
        'featured': featured,
        'active': 'active',
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
    return render(request, 'store/shop-list.html', context)


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


#blog views
class BlogListView(ListView):
    model=BlogPost
    template_name = 'store/blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['blogs'] = self.model.objects.filter(is_active=True).order_by('-created')
        context['side_bar'] = self.model.objects.all().order_by('?')[:3]
        context['page'] = 'Our Blogs'
        return context


class BlogPostDetailView(HitCountDetailView):
    model = BlogPost
    template_name = 'store/blog-details.html'
    count_hit = True
    context_object_name = 'blog'
    
    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        get_current_id = self.model.objects.filter(slug=self.kwargs['slug']).first()
        context['next'] = self.model.objects.filter(id__gt=get_current_id.pk).first()
        context['previous'] = self.model.objects.filter(id__lt=get_current_id.pk).first()
        context['other'] = self.model.objects.exclude(slug=self.kwargs['slug'])[:3]
        context['blog_cat'] = Category.objects._mptt_filter(
            blog_cats__in=self.model.objects.all().distinct()
        )
        return context
    

class BlogListCategoryView(View):

    def get(self, request, blog_slug):
        blogs = BlogPost.objects.filter(
            category__in=Category.objects.get(slug=blog_slug).get_descendants(include_self=True)
        )
        other = BlogPost.objects.all().order_by('?')[:3]
        context = {
            'blogs': blogs,
            'side_bar': other,
            'page': 'filtered by {} category'.format(blog_slug)
        }
        return render(request, 'store/blog.html', context)
    


#contact page
def contactView(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'], 
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = '''
            From : {}
            Email: {}
            Subject: {}
            
            Message:
            {}
            '''.format(data['name'], data['email'], data['subject'], data['message'])
            email = EmailMessage(data['subject'], message, data['email'], [settings.EMAIL_RECEIPIENT])
            # EmailThread(email).start()
            email.send(fail_silently=False)
            return render(request, 'nailspar/contacts.html', {'name': data['name']})
    else:
        form = ContactForm()

    about = About.objects.first()
    context ={
        'form': form,
        'about': about,
    }
    return render(request, 'store/contact.html', context)

