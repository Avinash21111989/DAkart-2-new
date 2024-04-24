from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from store.models import Product

# Create your views here.
#my views
def cart_id(request):
    cartId = request.session.session_key
    if not cartId:
        cartId = request.session.create()
    return cartId

def add_cart(request,product_id):
    
    product = Product.objects.get(id=product_id)
  
    try:
        cart = Cart.objects.get(cart_id = cart_id(request))
        if request.user.is_authenticated:
            try:
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists == True:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = request.user
                        item.save()
        
            except:
                pass
        else:
            print("in else")

            cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
            print("check for true",cart_item_exists)
            print(  )
            print(cart)
            if cart_item_exists == True:
                cart_item = CartItem.objects.filter(product=product,cart=cart)
                for item in cart_item:
                        item.save()
            else:
                print("in else")


            
        
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = cart_id(request)
        )
        
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
        
    except CartItem.DoesNotExist:
      
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                    product= product,
                    quantity = 1,
                    user = request.user
                )
        else:
            print("in else condition")
            cart_item = CartItem.objects.create(
                product= product,
                quantity = 1,
                cart = cart
            )

    return redirect('cart')

def carts(request, total=0,tax=0):
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    else:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        
    tax = (2 * total)/100
    grand_total = total +  tax
    context = {
        'total':total,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }

    return render(request,'carts.html',context)

def remove_cartItem(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id = cart_id(request))
    cart_item = CartItem.objects.get(product=product,cart = cart)

    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def checkout(request,total=0):
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart,is_active=True)
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity

    context = {
       'total':total,
       'cart_items':cart_items, 
    }

    return render(request,'checkout.html', context)



