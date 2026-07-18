from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon

# Create your views here.

@require_POST
def coupon_apply(request):
    now = timezone.now()
    
    if request.method == 'POST':
        form = CouponApplyForm(data=request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist: 
                request.session['coupon_id'] = None
    else:
        form = CouponApplyForm()
    
    return redirect('cart-detail')