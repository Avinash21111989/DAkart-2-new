from . views import cart_id
from . models import Cart,Cartitem



def cartCounter(request):
  cart_count = 0
  try:
      cart = Cart.objects.get(cart_id = cart_id(request))
      cart_items = Cartitem.objects.filter(cart = cart,is_active=True) 
      for cart_item in cart_items:
        cart_count +=  cart_item.quantity
  except Cart.DoesNotExist:
      cart_count = 0
     

  return dict(count = cart_count)    


                                                                        #  contextprocessor always return in dict
                                                                        # get will fetch single record but filter will fetch multiple record