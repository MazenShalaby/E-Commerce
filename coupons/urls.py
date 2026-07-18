from django.urls import path

from .views import coupon_apply
# create your urlpatterns here.


urlpatterns = [
    path('apply/', coupon_apply, name='coupon-apply'),
]
