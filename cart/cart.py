from decimal import Decimal
from django.conf import settings

from inventory.models import Product
from coupons.models  import Coupon
from .models import Cart as CartModel, CartItem
from .forms import CartAddForm

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
        if not self.request.user.is_authenticated:
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

    def clear_coupon_if_cart_empty(self):
        if self.request.user.is_authenticated:
            if not self.db_cart.items.exists():
                self.db_cart.coupon = None
                self.db_cart.save(update_fields=["coupon"])
        else:
            if not self.cart:
                self.session["coupon_id"] = None
            
    def remove(self, product):
        if self.request.user.is_authenticated:
            self.db_cart.items.filter(product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]

        self.clear_coupon_if_cart_empty()
        self.save()
        
    def clear(self):
        if self.request.user.is_authenticated:
            self.db_cart.items.all().delete()
        else:
            self.cart.clear()

        self.clear_coupon_if_cart_empty()
        self.save()


    def __iter__(self): 

        if self.request.user.is_authenticated:
            for item in self.db_cart.items.select_related("product"):
                yield {
                    "product": item.product,
                    "price": item.product.price,
                    "quantity": item.quantity,
                    "total_price": item.product.price * item.quantity,
                    "update_item_quantity": CartAddForm(
                        initial={
                            "quantity": item.quantity,
                            "override": True,
                        }
                    ),
                }
        else:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart = self.cart.copy()

            for product in products:
                cart[str(product.id)]["product"] = product

            for item in cart.values():
                item["price"] = Decimal(item["price"])
                item["total_price"] = item["price"] * item["quantity"]
                item["update_item_quantity"] = CartAddForm(
                    initial={
                        "quantity": item["quantity"],
                        "override": True,
                    }
                )
                yield item

    def get_total_price(self):
        if self.request.user.is_authenticated:
            return sum(
                item.product.price * item.quantity for item in self.db_cart.items.select_related("product")
            )

        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def __len__(self):
        if self.request.user.is_authenticated:
            return sum(item.quantity for item in self.db_cart.items.all())
        return sum(item["quantity"] for item in self.cart.values())

    @property
    def coupon(self):
        if self.request.user.is_authenticated:
            return self.db_cart.coupon

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

    def set_coupon(self, coupon):
        if self.request.user.is_authenticated:
            self.db_cart.coupon = coupon
            self.db_cart.save(update_fields=['coupon'])
        else:
            self.session['coupon_id'] = coupon.id
            self.save()

    def clear_coupon(self):
        if self.request.user.is_authenticated:
            self.db_cart.coupon = None
            self.db_cart.save(update_fields=['coupon'])
        else:
            self.session["coupon_id"] = None
            self.save()