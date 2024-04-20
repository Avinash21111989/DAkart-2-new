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

]