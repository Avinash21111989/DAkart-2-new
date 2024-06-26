from django.urls import path, include

from . import views 

urlpatterns = [
    path('',views.store, name="store"),
    path('category/<slug:category_url>',views.store,name='products_by_category'),
    path('category/<slug:category_url>/<slug:product_url>',views.product_detail,name="product_details"),
    path('search',views.search,name="search"),
    path('submit_review/<int:product_id>',views.submit_review,name="myrating"),
]