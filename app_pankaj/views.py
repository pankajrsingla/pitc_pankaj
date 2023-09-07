from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, ServiceProvider, Order, AccountManager

def list_customers(request):
    customers = Customer.objects.all()
    return render(request, 'list_customers.html', {'customers': customers})

def list_service_providers(request):
    service_providers = ServiceProvider.objects.all()
    return render(request, 'list_service_providers.html', {'service_providers': service_providers})

def list_orders(request):
    orders = Order.objects.all()
    return render(request, 'list_orders.html', {'orders': orders})

def add_service_to_order(request, order_id, service_provider_id, account_manager_id):
    order = Order.objects.get(pk=order_id)
    service_provider = ServiceProvider.objects.get(pk=service_provider_id)
    account_manager = AccountManager.objects.get(pk=account_manager_id)
    
    try:
        order.add_service(service_provider, account_manager)
        order.save()
        return HttpResponse("Service added to order successfully!")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
