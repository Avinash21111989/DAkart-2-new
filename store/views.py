from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from django.db import connection

# Create your views here.

def store(request,category_url=None):

    if category_url != None:
        categories = get_object_or_404(Category, slug=category_url)
        products = Product.objects.filter(category=categories,is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    context = {
        'products':products,
        'product_count':product_count
        
    }

    return render(request,'store.html',context)

def product_detail(request,category_url,product_url):
    
    try:
        single_product = Product.objects.get(category__slug=category_url,slug=product_url)
        #print(Product.objects.get(category__slug=category_url,slug=product_url).query)
    except:
        pass
        
        
    context = {
        'single_product':single_product
    }
    
    return render(request,'product_detail.html', context)