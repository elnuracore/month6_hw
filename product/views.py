
from rest_framework.decorators import api_view as shop_api
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import (CategoryListSerializer, 
                          ProductListSerializer, 
                          ReviewListSerializer, 
                          CategoryDetailSerializer,
                          ProductDetailSerializer,
                          ReviewDetailSerializer,
                          ProductReviewsSerializer,
                          ProductCreateSerializer)
                
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from common.permissions import IsOwner, IsAnonymous, CanEditSomeTime, IsModerator
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
class CategoryListAPIView(ListCreateAPIView):
    serializer_class=CategoryListSerializer
    queryset=Category.objects.all()
    pagination_class=PageNumberPagination
    
class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        cached_data = cache.get("products_list")
        if cached_data:
            print("Cached_data SUCCESS, REDIS")
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().get(self, request, *args, **kwargs)
        print("Used Postgres")
        if response.data.get("total", 0) > 0:
            cache.set("products_list", response.data, timeout=300)
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class ReviewListAPIView(ListCreateAPIView):
    serializer_class=ReviewListSerializer
    queryset=Review.objects.all()
    pagination_class=PageNumberPagination

class ProductReviewListAPIView(ListAPIView):
    serializer_class=ProductReviewsSerializer
    queryset=Product.objects.all()
  
class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=CategoryDetailSerializer
    queryset=Category.objects.all()
    lookup_field='id'
    permission_classes=[IsOwner | IsAnonymous | IsModerator]
 

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied("You can only edit your own products")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You can only delete your own products")
        instance.delete()
    
class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=ReviewDetailSerializer
    queryset=Review.objects.all()
    lookup_field='id'
