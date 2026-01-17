from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('products/', views.product_list),                # Function Based View
    path('products/', views.ProductListCreatAPIView.as_view()),  # Class Based View
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
]


# For ViewSet and Router I don't need to define each endpoint (e.g. {prefix}/{url_path}, {prefix}/{lookup}/) separately
# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls