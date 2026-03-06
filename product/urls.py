from django.urls import path
from . import views

urlpatterns = [
    # path('categories/', views.category_list_api_view),
    # path('categories/<int:id>/', views.category_detail_api_view),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()), 

    # path('products/', views.product_list_api_view),
    # path('products/<int:id>/', views.product_detail_api_view),
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),
    

    # path('reviews/', views.review_list_api_view),
    # path('reviews/<int:id>/', views.review_detail_api_view),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),

    # path('products/<int:product_id>/reviews/', views.review_list_product_api_view),
    path('products/<int:product_id>/reviews/', views.ProductReviewListAPIView.as_view()),
]