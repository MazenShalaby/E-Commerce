from decimal import Decimal

from django.conf import settings

from inventory.models import Product
from coupons.models  import Coupon
from .models import Cart as CartModel
from .models import CartItem
from .forms import CartAddForm

# create your cart here.


class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.session_cart = self.session.setdefault(settings.CART_SESSION_ID, {})
        self.coupon_id = self.session.get('coupon_id')
        
        if request.user.is_authenticated:
            self.db_cart, _ = CartModel.objects.get_or_create(user=request.user)

    def save(self):
        if not self.request.user.is_authenticated:
            self.session.modified = True

    def merge_session_cart(self):
        if not self.request.user.is_authenticated:
            return
        
        if not self.session_cart: # Avoid an unnecessary merge
            return
        
        for product_id, item in self.session_cart.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue
            
            cart_item, _ = CartItem.objects.get_or_create(
                cart=self.db_cart,
                product=product,
                defaults={'quantity': 0}
            )
            
            cart_item.quantity += item['quantity']
            cart_item.save(update_fields=["quantity"])
        
        self.session_cart.clear()
        self.session['coupon_id'] = None
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        if self.request.user.is_authenticated:
            item, _ = CartItem.objects.get_or_create(
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
            item = self.session_cart.setdefault(
                product_id,
                {"quantity": 0, "price": str(product.price)},
            )

            if override_quantity:
                item["quantity"] = quantity
            else:
                item["quantity"] += quantity
            self.save()


    def remove(self, product):
        if self.request.user.is_authenticated:
            self.db_cart.items.filter(product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.session_cart:
                del self.session_cart[product_id]
        self.remove_coupon()
        self.save()
        
    def clear(self):
        if self.request.user.is_authenticated:
            self.db_cart.items.all().delete()
        else:
            self.session_cart.clear()
        self.remove_coupon()
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
            product_ids = self.session_cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart = self.session_cart.copy()

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

    def __len__(self):
        if self.request.user.is_authenticated:
            return sum(item.quantity for item in self.db_cart.items.all())
        return sum(item["quantity"] for item in self.session_cart.values())

    def get_total_price(self):
        if self.request.user.is_authenticated:
            return sum(
                item.product.price * item.quantity for item in self.db_cart.items.select_related("product")
            )
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.session_cart.values()
        )
        
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

    @property
    def coupon(self): # getter
        if self.request.user.is_authenticated:
            return self.db_cart.coupon

        if not self.coupon_id: # Avoid an unnecessary database query of the next line
            return None

        try:
            return Coupon.objects.get(id=self.coupon_id)
        except Coupon.DoesNotExist:
            return None

    def set_coupon(self, coupon): # setter
        if self.request.user.is_authenticated:
            self.db_cart.coupon = coupon
            self.db_cart.save(update_fields=['coupon'])
        else:
            self.session['coupon_id'] = coupon.id
            self.save()

    def clear_coupon(self): # remover
        if self.request.user.is_authenticated:
            self.db_cart.coupon = None
            self.db_cart.save(update_fields=['coupon'])
        else:
            self.session["coupon_id"] = None
            self.save()

    def remove_coupon(self):
        if self.request.user.is_authenticated:
            if not self.db_cart.items.exists():
                self.db_cart.coupon = None
                self.db_cart.save(update_fields=["coupon"])
        else:
            if not self.session_cart:
                self.session["coupon_id"] = None
                self.save()