from cart.cart import Cart

# create your context processors here.

def cart(request):
    context = {'cart': Cart(request)}
    return context