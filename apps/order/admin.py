import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Order, OrderItem


def order_name(obj):
    return '%s %s' % (obj.first_name, obj.last_name)
order_name.short_description = 'Name'

def admin_order_staged(modeladmin, request, queryset):
    for order in queryset:
        order.status_date_changed = timezone.now()
        order.status = Order.STAGED
        order.save()
    return
admin_order_staged.short_description = 'Set Staged'

def admin_order_prepared(modeladmin, request, queryset):
    for order in queryset:
        order.status_date_changed = timezone.now()
        order.status = Order.PREPARED
        order.save()
    return
admin_order_prepared.short_description = 'Set Prepered'

def admin_order_dispatched(modeladmin, request, queryset):
    for order in queryset:
        order.status_date_changed = timezone.now()
        order.status = Order.DISPATCHED
        order.save()
        
        html = render_to_string('order_sent.html', {'order': order})
        send_mail('Order dispatched', 
                  'Your order has been dispatched and will be delivered to you within next 6 hours!', 
                  'noreply@ecf-vegbox.com', 
                  ['mail@ecf-vegbox.com', order.email], 
                  fail_silently=False,
                  html_message=html)
    return
admin_order_dispatched.short_description = 'Set Dispatched'

def admin_order_delivered(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = timezone.now()
        order.status = Order.DELIVERED
        order.save()
        send_mail('Order delivered', 
                  'Your order has been delivered!', 
                  'noreply@ecf-vegbox.com', 
                  ['mail@ecf-vegbox.com', order.email], 
                  fail_silently=False)
    return
admin_order_delivered.short_description = 'Set Delivered'

def admin_order_returned(modeladmin, request, queryset):
    for order in queryset:
        order.status_date_changed = timezone.now()
        order.status = Order.RETURNED
        order.save()
    return
admin_order_returned.short_description = 'Set Returned'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'created_at', 'status', 'status_date_changed', 'shipped_date',]
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInline]
    actions = [admin_order_staged, 
               admin_order_prepared, 
               admin_order_dispatched,
               admin_order_delivered,
               admin_order_returned]
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.disable_action('delete_selected')
