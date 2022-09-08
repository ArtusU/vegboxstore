import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.cart.webhook import webhook
from apps.cart.views import cart_detail, success
from apps.core.views import frontpage, contact, about
from apps.coupon.api import api_can_use
from apps.store.views import product_detail, category_detail
from apps.store.api import api_add_to_cart, api_remove_from_cart, checkout_session


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', frontpage, name='frontpage'),
    path('cart/', cart_detail, name='cart_detail'),
    path('hooks/', webhook, name='webhook'),
    path('cart/success/', success, name='success'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    
    path('api/can_use/', api_can_use, name='api_can_use'),
    
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/checkout/session/', checkout_session, name='create_checkout_session'),
    
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:slug>/', category_detail, name='category_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
