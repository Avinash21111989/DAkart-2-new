from django.urls import path, include

from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('signin/',views.signin,name="signin"),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('logout/',views.logout,name="logout"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('my_orders/',views.my_orders,name="my_orders"),
    path('order_detail/<int:order_number>',views.order_detail,name="order_detail"),

]