from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='img')
    location = models.TextField(max_length=80)

    def interest_count(self):
        interest = Interest.objects.filter(product = self)
        count = len(interest)
        return count

class Interest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.TextField(max_length=80)
    email = models.EmailField()
    location = models.TextField(max_length=80)

    class Meta:
        unique_together = (('product', 'email'),)