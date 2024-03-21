from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def listproduct(request):
    context = {
        "name":"T-Shirt",
        "size":"Medium"
    }
    
    return render(request,"product.html",context)

def editProduct(request):
    return HttpResponse("Edit your product here")