#!venv/bin/python

import os
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 
from django.http import HttpResponse

# Define the ServiceProvider model to represent companies offering services.
class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields relevant to service providers here
    
    def __str__(self):
        return self.name
    
# Define the Customer model for users who use the platform.
class Customer(models.Model):
    # Link to the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.user.username

# Define the AccountManager model for users with account manager roles.
class AccountManager(models.Model):
    # Link to the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

    def managed_service_providers(self):
        # Define a method to get the managed service providers for this account manager
        return ServiceProvider.objects.filter(accountmanager=self)


# Define the Order model to represent customer orders.
class Order(models.Model):
    # Link to the Customer who placed the order
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    # Define a many-to-many relationship with ServiceProvider for services in the order.
    services = models.ManyToManyField(ServiceProvider)
    
    # Add other fields relevant to the order here

    # Add a foreign key to link each order to its managing account manager
    account_manager = models.ForeignKey(AccountManager, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Order for {self.customer.user.username}"

    # Custom method to add a service to the order while enforcing constraints
    def add_service(self, service_provider, account_manager):
        # Check if the service provider is managed by the provided account manager
        if service_provider in account_manager.managed_service_providers():
            self.services.add(service_provider)
            # Set the account manager for this order
            self.account_manager = account_manager 
        else:
            raise Exception("Cannot add service from unmanaged provider.")

# Example view to add a service to an order
def add_service_to_order(order_id, service_provider_id, account_manager_id):
    # Retrieve the order, service provider, and account manager
    order = get_object_or_404(Order, pk=order_id)
    service_provider = get_object_or_404(ServiceProvider, pk=service_provider_id)
    account_manager = get_object_or_404(AccountManager, pk=account_manager_id)
    
    try:
        # Attempt to add the service to the order using the add_service method
        order.add_service(service_provider, account_manager)
        order.save()
        return HttpResponse("Service added to order successfully!")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")