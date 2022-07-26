from django.db import models
from django.contrib.auth.models import User

from apps.store.models import Product

class Order(models.Model):
    ORDERED = 'ordered' 
    STAGED = 'staged'
    PREPARED = 'prepared'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'
    RETURNED = 'returned'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'), 
        (STAGED, 'Staged'), 
        (PREPARED, 'Prepared'),
        (DISPATCHED, 'Dispatched'),
        (DELIVERED, 'Delivered'), 
        (RETURNED, 'Returned')
    )
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    used_coupon = models.CharField(max_length=50, blank=True, null=True)
    payment_intent = models.CharField(max_length=255)
    shipped_date = models.DateTimeField(blank=True, null=True)
    status_date_changed = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=ORDERED)
    
    def __str__(self):
        return self.first_name
    
    def get_total_quantity(self):
        return sum(int(item.quantity) for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)
