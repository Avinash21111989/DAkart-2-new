from django.urls import path, include

from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('signin/',views.signin,name="signin"),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('logout/',views.logout,name="logout"),

]