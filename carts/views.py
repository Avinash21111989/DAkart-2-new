from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from store.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
#my views
def cart_id(request):
    cartId = request.session.session_key
    if not cartId:
        cartId = request.session.create()
    return cartId

def add_cart(request,product_id):
    print("function called")
    product = Product.objects.get(id=product_id)
  
    try:
            cart = Cart.objects.get(cart_id = cart_id(request))
    except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = cart_id(request)
            )
        
    if request.user.is_authenticated:
            cart_item_exists = CartItem.objects.filter(product=product,user=request.user).exists()
            print("exists",cart_item_exists)
            if cart_item_exists:
                cart_items =  CartItem.objects.filter(product=product,user=request.user)
                for item in cart_items:
                    item.quantity +=1
                    item.save()
            else:
                print("new record ")
                item = CartItem.objects.create(product=product,quantity=1,user=request.user)
                item.save()
    else:
            cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
            if cart_item_exists:
                cart_items =  CartItem.objects.filter(product=product,cart=cart)
                for item in cart_items:
                    item.quantity +=1
                    item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)


    return redirect('cart')

def carts(request, total=0,tax=0,cart_items=None):
            try:
                if request.user.is_authenticated:
                    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
                else:
                    cart = Cart.objects.get(cart_id=cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart,is_active=True)
            except:
                pass
            
    
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
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id = cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart = cart)

    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='signin')
def checkout(request,total=0,cart_items=None):
    try:
        if request.user.is_authenticated:
             cart_items = CartItem.objects.filter(user=request.user,is_active=True)

        else:     
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
    except:
         pass
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity

    context = {
       'total':total,
       'cart_items':cart_items, 
    }

    return render(request,'checkout.html', context)



