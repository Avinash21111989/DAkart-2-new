from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from Order.models import Order, OrderProduct
from accounts.models import UserProfile
from carts.models import Cart, CartItem
from . forms import RegistrationForm,UserProfileForm, UserForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from carts.views import cart_id

def register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("check here",form.errors)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            password = form.cleaned_data['password']

            user_isactive = User.objects.filter(email=email)
            if user_isactive.exists() == False:       
                user = User.objects.create_user (
                    username = username,
                    first_name =  first_name,
                    last_name  = last_name,
                    email  = email,
                    password = password,
                    is_active = False
                )
                user.save()

                #create a user profile
                profile = UserProfile()
                profile.user_id = user.id
                profile.profile_picture = 'default/default-user.png'
                profile.save()
            
                current_site = get_current_site(request)
                mail_subject = "DAKart - please activate your account"
                email_from = settings.EMAIL_HOST_USER
                message = render_to_string('accounts/account_verfication_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user)
                })
                to_email = [email,]
                send_mail(mail_subject,message,email_from,to_email)
                return redirect('/accounts/signin?command=verification&email='+email)
            else:
                messages.warning(request,"Email id already exists. Please enter another email")
                context = {
               'form': form
                }
                return render(request,'accounts/register.html', context)
        else:
            context = {
               'form': form
            }
            return render(request,'accounts/register.html', context)
    form = RegistrationForm(request.POST)    
    context = {
               'form': form
            }
    return render(request,'accounts/register.html', context)

def signin(request):
    
    if request.method == 'POST':
        is_cart_item_exists = None    
        entered_username = request.POST['username']
        entered_password = request.POST['password']
        
        user = auth.authenticate(username = entered_username, password = entered_password)
        
        if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                except:
                    pass
                if is_cart_item_exists:
                    print("cart exists")
                    cart_item = CartItem.objects.filter(cart=cart,is_active=True)
                    print(cart_item)
                    for item in cart_item:
                                item.user = user
                                item.save()
                auth.login(request,user)
                return redirect("welcome")
        else:
            user_isactive = User.objects.filter(username=entered_username,is_active=True)
            if user_isactive.exists() == False:
                messages.warning(request,"Your account is not activated. Please activate your account")
            else:
                messages.warning(request,"Invalid credetials")
    return render(request,'accounts/signin.html') 

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('signin')
    else:
        return redirect('register')
    

def logout(request):
    auth.logout(request)
    messages.success(request,"you have been logged out")
    return redirect('signin')

@login_required(login_url='signin')
def dashboard(request,userprofile=None):
    try:
        userprofile = UserProfile.objects.get(user_id = request.user.id)
    except:
        pass
    orders = Order.objects.filter(user = request.user, is_ordered= True)
    OrdersCount = orders.count()
    context = {
        'userprofile':userprofile,
        'OrdersCount': OrdersCount
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='signin')
def edit_profile(request):
    user_profile = None
    try:
        user_profile = UserProfile.objects.get(user_id = request.user.id)
    except:
        pass

    
    if request.method == 'POST':
        
        user_form = UserForm(request.POST,instance=request.user)
        user_profile_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)

        if  user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request,"Your profile has been updated!")
            return redirect('edit_profile')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance = user_profile)
    context = {
        'user_form':user_form,
        'user_profile_form':user_profile_form,
        'user_profile':user_profile
    }
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url ='signin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        print(current_password)
        print(new_password)
        print(confirm_new_password)
        user = User.objects.get(username__iexact=request.user.username)
        if new_password == confirm_new_password:
            print("first validation")
            check_password = user.check_password(current_password)
            print("check_password",check_password)
            if check_password:
                user.set_password(new_password)
                user.save()
                auth.logout(request)
            else:
                messages.warning(request,"please enter a valid current password")
   
        else:
            messages.warning(request,"new password and confirm password not matching")


    return render(request,'accounts/change_password.html')

def my_orders(request):
    Orders = Order.objects.filter(user= request.user,is_ordered= True)
    context = {
       'Orders':Orders

    }

    return render (request,'accounts/my_orders.html',context)

def order_detail(request,order_number):
    order_detail = OrderProduct.objects.filter(order__order_number = order_number)

    order = Order.objects.get(order_number = order_number)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    
    context = {
        'order_detail':order_detail,
        'subtotal':subtotal,
        'order':order
    }

    return render(request,'accounts/order_detail.html',context)


