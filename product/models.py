from django.db import models
from users.models import CustomUser
from common.models import BaseModel

class Category(BaseModel):
    name=models.CharField(max_length=255, default="unknown")
    
    def __str__(self):
       return self.name or f'{self.pk}'


class Product(BaseModel):
    title=models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)
    price=models.IntegerField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    owner=models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    def __str__(self):
       return f' {self.title} - {self.category}'
   
class Review(models.Model):
    text=models.TextField(null=True, blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='reviews' )
    STARS=(
    (i, '*' * i) for i in range(1, 6)
)
    stars=models.IntegerField(choices=STARS, default=5, null=True)
    @property
    def reviews_name(self):
      return [i.name for i in self.reviews.all()]
    
    def __str__(self):
       return f'{self.product} : {self.text}- {self.stars}'
   
