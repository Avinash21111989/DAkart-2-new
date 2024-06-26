from django.contrib import admin
from store.models import Product 
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','slug','price','stock','category','modified_date')
    prepopulated_fields = {'slug':('product_name',)}
admin.site.register(Product,ProductAdmin)