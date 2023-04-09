from datetime import datetime

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from order.models import Order

# Create your views here.

User = get_user_model()

@login_required
def ordersDashboard(request):
    users = User.objects.all().count()
    orders = Order.objects.all()
    total_orders = orders.count()
    pending_orders = orders.filter(order_status='Pending')
    total_pending = pending_orders.count()
    todays_orders = orders.filter(created=datetime.today())
    revenue = orders.aggregate(Sum('total_paid'))
    context ={
        'users': users,
        'orders':orders,
        'total_orders':total_orders,
        'pending_orders': pending_orders,
        'total_pending': total_pending,
        'todays_orders': todays_orders,
        'revenue': revenue,
    }
    return render(request, 'dashboard/index2.html', context)