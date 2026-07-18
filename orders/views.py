from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from .forms import OrderCreateForm, OrderPaymentForm
from .models import Order, OrderItem, OrderPayment
from cart.cart import Cart

# Create your views here.


def order_create(request):

    cart = Cart(request)
    created = False

    if cart:
        if request.method == "POST":
            form = OrderCreateForm(data=request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )

                # Order Placement Mail
                subject = "Order Placement"
                message = f"Your Order with ID: {order.order_id} has been placed.\nOrder Detail:\n"
                for item in cart:
                    product_name = item["product"].name
                    product_price = item["price"]
                    product_quantity = item["quantity"]
                    message += f"\nProduct Name: {product_name}\nProduct Price: {product_price}\nProduct Quantity: {product_quantity}\n"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [order.email]
                send_mail(subject, message, from_email, recipient_list)

                cart.clear()
                created = True
                return redirect("order-payment", order_id=order.id)
        else:
            form = OrderCreateForm()
            context = {"form": form}
            return render(request, "orders/order_create.html", context)
    else:
        return HttpResponse("No items within the cart!")


def order_payment(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = OrderPaymentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order.paid = True
            order.save()
            payment_form = form.save(commit=False)
            payment_form.order = order
            payment_form.save()
            return redirect('success-payment', order_id=order.id)
    else:
        form = OrderPaymentForm()
    
    context = {'form': form}
    return render(request, 'orders/order_payment.html', context)


def success_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    context = {'order': order}
    return render(request, 'orders/success_payment.html', context)