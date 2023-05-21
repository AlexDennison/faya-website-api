from django.urls import path
from .import views

urlpatterns = [
    path('customer/create', views.CustomerCreate.as_view()),
    path('customer/update/<int:pk>', views.CustomerUpdate.as_view()),
    path('customer/list', views.CustomerList.as_view()),
    path('customer/detail/<int:pk>', views.CustomerDetail.as_view()),
    path('customer/delete/<int:pk>', views.CustomerDelete.as_view()),
    path('product/create', views.ProductCreate.as_view()),
    path('product/update/<int:pk>', views.ProductUpdate.as_view()),
    path('product/list', views.ProductList.as_view()),
    path('product/detail/<int:pk>', views.ProductDetail.as_view()),
    path('product/delete/<int:pk>', views.ProductDelete.as_view()),
]
