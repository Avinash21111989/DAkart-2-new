

from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, Cartitem
from store.models import Product

# Create your views here.

def cart_id(request):
  cart_id = request.session.session_key
  if not cart_id:
    cart_id = request.session.create()
  return cart_id

def add_cart(request, product_id):
  product = Product.objects.get(id = product_id)
  print("product value : ", product)

  try: 
      cart = Cart.objects.get(cart_id = cart_id(request))
      

  except Cart.DoesNotExist:
    cart = Cart.objects.create(               # create the session id 
      cart_id = cart_id(request)

    )
    
  try:

    cart_item = Cartitem.objects.get(product=product,cart=cart)
    cart_item.quantity +=1 
    cart_item.save()
  except Cartitem.DoesNotExist:

    cart_item = Cartitem.objects.create(
      product = product,
      quantity = 1,
      cart = cart
    )
  return redirect('cart')

def cart(request,total=0,tax=0):
    cart = Cart.objects.get(cart_id = cart_id(request))
    cart_items =  Cartitem.objects.filter(cart = cart,is_active = True)
    for cart_item in cart_items:
      total += cart_item.product.price * cart_item.quantity
    
    tax = (2 * total)/100
    grand_total = total + tax
    context = {
      "total": total, 
      "cart_items": cart_items,
      "tax": tax,
      "grand_total": grand_total


    }
    return render(request,"carts.html",context)


def remove_cartitem(request,product_id):
  product =get_object_or_404(Product, id=product_id)
  cart = Cart.objects.get(cart_id = cart_id(request))
  cart_item = Cartitem.objects.get(product=product,cart=cart)

  if cart_item.quantity >1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()
  return redirect('cart')

def delete_cart(request,product_id):
  product =get_object_or_404(Product, id=product_id)
  cart = Cart.objects.get(cart_id = cart_id(request))
  cart_item = Cartitem.objects.get(product=product,cart=cart)

  cart_item.delete()
  return redirect('cart')




