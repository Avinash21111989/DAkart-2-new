from django.urls import path
from .import views
# testing main
urlpatterns = [
    path('',views.carts,name="cart"),
    path('add_cart/<int:product_id>/',views.add_cart,name='addcart')
]