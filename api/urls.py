from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.product_list),                # Function Based View
    path('products/', views.ProductListAPIView.as_view()),  # Class Based View
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('orders/user/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]