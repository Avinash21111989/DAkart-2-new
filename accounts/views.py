from django.shortcuts import render
from . forms import RegistrationForm
from django.contrib.auth.models import User

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
                password = password
            )
            user.save()
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
    pass