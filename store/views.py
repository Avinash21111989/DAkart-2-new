
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import category  

def store(request, category_url=None):
    
    categories = None  
    
    if category_url is not None:
       
        categories = get_object_or_404(category, slug=category_url)
       
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
        
        
    else:
        products = Product.objects.filter(is_available=True)
    
        product_count = products.count()
    
    context = {
        "products": products,
        "product_count": product_count,
        
    }
    
    return render(request, "store.html", context)


def product_detail(request,category_url,product_url):
    single_product= Product.objects.get(category__slug=category_url,slug=product_url)
    
    

    context = {
        'single_product': single_product
        
    }
    return render (request,"product_detail.html",context)
    


