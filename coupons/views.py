from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon
from cart.cart import Cart

# Create your views here.

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    cart = Cart(request)

    if form.is_valid():
        code = form.cleaned_data.get("code")
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            cart.set_coupon(coupon)
        except Coupon.DoesNotExist:
            cart.clear_coupon()

    return redirect("cart-detail")