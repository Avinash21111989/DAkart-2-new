from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from . forms import RegistrationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

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
            user = User.objects.create_user (
                username = username,
                first_name =  first_name,
                last_name  = last_name,
                email  = email,
                password = password,
                is_active = False
            )
            user.save()

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