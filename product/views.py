
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
class CategoryListAPIView(ListCreateAPIView):
    serializer_class=CategoryListSerializer
    queryset=Category.objects.all()
    pagination_class=PageNumberPagination
    
class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [ IsOwner | IsAnonymous | IsModerator]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    permission_classes = [ (IsOwner | IsAnonymous | IsModerator), CanEditSomeTime] 
    
class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=ReviewDetailSerializer
    queryset=Review.objects.all()
    lookup_field='id'

# @shop_api(['GET', 'POST'])
# def category_list_api_view(request):
#     if request.method == 'GET':
#         categories=Category.objects.all()
#         data= CategoryListSerializer(categories, many=True).data 
#         return Response(
#             data=data,
#     )
#     elif request.method == 'POST':
#         serializer=CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
        
#         name=serializer.validated_data.get('name')
#         categories=Category.objects.create(name=name)
        
#     return Response(status=status.HTTP_201_CREATED,
#                         data=CategoryDetailSerializer(categories).data)
        

# @shop_api(['GET', 'POST'])
# def product_list_api_view(request):
#     if request.method == 'GET':
#         products=Product.objects.all()
#         data= ProductListSerializer(products, many=True).data 
#         return Response(
#           data=data,
#           )
#     elif request.method == 'POST':
#         serializer=ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#         title=serializer.validated_data.get('title')
#         description=serializer.validated_data.get('description')
#         price= serializer.validated_data.get('price')
#         category_id=serializer.validated_data.get('category_id')
#         products=Product.objects.create(
#             title=title,
#             description=description,
#             price=price,
#             category_id=category_id
#         )
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ProductDetailSerializer(products).data)
          
# @shop_api(['GET', 'POST'])
# def review_list_api_view(request):
#     if request.method == 'GET':
#         reviews=Review.objects.all()
#         data= ReviewListSerializer(reviews, many=True).data 
#         return Response(
#         data=data,
#          )
#     elif request.method == 'POST':
#         serializer=ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#         text=serializer.validated_data.get('text')
#         product_id=serializer.validated_data.get('product_id')
#         stars=serializer.validated_data.get('stars')
#         reviews=Review.objects.create(
#             text=text,
#             product_id=product_id,
#             stars=stars
#         )
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ReviewDetailSerializer(reviews).data)
# @shop_api(['GET'])
# def review_list_product_api_view(request):
#     rating=Product.objects.all()
#     data=ProductReviewsSerializer(rating, many=True).data
#     return Response(
#         data=data,
#     )
# @shop_api(['GET', 'PUT', 'DELETE'])
# def category_detail_api_view(request, id):
#     try:
#         categories=Category.objects.get(id=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND,
#                         data={'error':'this category is not found!'})
#     if request.method == 'GET':
#         data=CategoryDetailSerializer(categories, many=False).data
#         return Response(data=data )
#     elif request.method == 'PUT':
#         serializer=CategoryValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         categories.name=serializer.validated_data.get('name')
#         categories.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=CategoryDetailSerializer(categories).data)
#     elif request.method == 'DELETE':
#         categories.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @shop_api(['GET', 'PUT', 'DELETE'])
# def product_detail_api_view(request, id):
#     try:
#         products=Product.objects.get(id=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND,
#                         data={'error':'this product is not found!'})
#     if request.method == 'GET':
#        data=ProductDetailSerializer(products, many=False).data
#        return Response(data=data )
#     elif request.method == 'PUT':
#         serializer=ProductValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         products.title=serializer.validated_data.get('title')
#         products.description=serializer.validated_data.get('description')
#         products.price=serializer.validated_data.get('price')
#         products.category_id=serializer.validated_data.get('category_id')
#         products.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ProductDetailSerializer(products).data)
#     elif request.method == 'DELETE':
#         products.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @shop_api(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         reviews=Review.objects.get(id=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND,
#                         data={'error':'this review is not found!'})
#     if request.method == 'GET':
#          data=ReviewDetailSerializer(reviews, many=False).data
#          return Response(data=data )
#     elif request.method == 'PUT':
#         serializer=ReviewValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         reviews.text=serializer.validated_data.get('text')
#         reviews.product_id=serializer.validated_data.get('product_id')
#         reviews.stars=serializer.validated_data.get('stars')
#         reviews.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ReviewDetailSerializer(reviews).data)
#     elif request.method == 'DELETE':
#         reviews.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
