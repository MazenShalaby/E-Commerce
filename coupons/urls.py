from django.urls import path

from .views import coupon_apply, coupon_remove

# create your urlpatterns here.


urlpatterns = [
    path('apply/', coupon_apply, name='coupon-apply'),
    path('remove/', coupon_remove, name='coupon-remove'),
]
