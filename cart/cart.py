from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.conf import settings

from inventory.models import Product
from coupons.models  import Coupon
from .models import Cart as CartModel, CartItem

# create your cart here.


class Cart:

    def __init__(self, request):
        self.request = request
        
        if request.user.is_authenticated:
            self.db_cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            self.session = request.session
            self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})
            self.coupon_id = self.session.get('coupon_id')

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):

        if self.request.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(
                cart=self.db_cart,
                product=product,
                defaults={"quantity": 0},
            )

            if override_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity

            item.save()

        else:
            product_id = str(product.id)
            item = self.cart.setdefault(
                product_id,
                {"quantity": 0, "price": str(product.price)},
            )

            if override_quantity:
                item["quantity"] = quantity
            else:
                item["quantity"] += quantity

            self.save()

    def _clear_coupon_if_cart_empty(self):
        if not self.cart:
            self.session['coupon_id'] = None
            
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self._clear_coupon_if_cart_empty()
        self.save()

    def clear(self):
        self.cart.clear()
        self._clear_coupon_if_cart_empty()
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def __len__(self):
        if self.request.user.is_authenticated:
            return sum(item.quantity for item in self.db_cart.items.all())
        return sum(item["quantity"] for item in self.cart.values())

    @property
    def coupon(self):
        if not self.coupon_id:
            return None

        try:
            return Coupon.objects.get(id=self.coupon_id)
        except Coupon.DoesNotExist:
            return None

    def get_total_after_discount(self): # base_price * (1 - percentage / 100)
        coupon = self.coupon
        if coupon:
            return round(self.get_total_price() * (1 - coupon.discount / Decimal(100)), 2)
        return self.get_total_price()
    
    def get_discounted_value(self): # value reduced from total price
        if self.coupon:
            return self.get_total_price() - self.get_total_after_discount()
        return Decimal(0)

    def get_sub_total(self, tax_value=20):
        if self.coupon:
            return self.get_total_after_discount() + tax_value
        return self.get_total_price() + tax_value