from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError
from common.validators import validator_birthdate


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model=Category
        fields='name products_count id'.split()
    def get_products_count(self, obj):
        return obj.product.count()
    
        
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='id title category price owner_id'.split()
        depth=1
        
    def get_reviews(self, product):
        return product.reviews_name()
    
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']
   
    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method == "POST":
                validator_birthdate(request)
        return attrs
  
class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='product text stars'.split()
class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = 'title category reviews rating'.split()
    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.count() == 0:
            return 0
        total = 0
        for review in reviews:
            total += review.stars
        return total / len(reviews)
   
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'

class CategoryValidateSerializer(serializers.Serializer):
    name=serializers.CharField(required=True, min_length=2, max_length=50)
    
    
class ProductValidateSerializer(serializers.Serializer):
    title=serializers.CharField(required=True, min_length=2, max_length=255)
    description=serializers.CharField(required=False)
    price=serializers.IntegerField()
    category_id=serializers.IntegerField(min_value=1)
    
    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('There is no such ID')
        return category_id
    
    
class ReviewValidateSerializer(serializers.Serializer):
    text=serializers.CharField(required=True, min_length=2, max_length=255)
    stars=serializers.IntegerField(default=5)
    product_id=serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('There is no such ID')
        return product_id