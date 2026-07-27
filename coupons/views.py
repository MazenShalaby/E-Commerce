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

    if form.is_valid():
        code = form.cleaned_data["code"]

        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )

            if request.user.is_authenticated:
                cart = Cart(request)
                cart.db_cart.coupon = coupon
                cart.db_cart.save(update_fields=["coupon"])
            else:
                request.session["coupon_id"] = coupon.id

        except Coupon.DoesNotExist:
            if request.user.is_authenticated:
                cart = Cart(request)
                cart.db_cart.coupon = None
                cart.db_cart.save(update_fields=["coupon"])
            else:
                request.session["coupon_id"] = None

    return redirect("cart-detail")