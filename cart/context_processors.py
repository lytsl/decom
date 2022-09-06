from cart.models import Cart, CartItem
from cart.views import _cart_id


def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for item in cart_items:
                count += item.quantity
        except Cart.DoesNotExist:
            count = 0
    return dict(cart_count=count)
