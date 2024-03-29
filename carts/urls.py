from  .import views
from django.urls import  path

urlpatterns = [
     path('',views.cart,name ="cart"),
     path('add_cart/<int:product_id>/',views.add_cart,name='addcart'),
     path('remove_cart_item/<int:product_id>/',views.remove_cartitem,name='Removecartitem'),
     path('delete_cart/<int:product_id>/',views.delete_cart,name='Deletecart'),
    



]