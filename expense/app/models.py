from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table="category"


class Expense(models.Model):
    amount = models.CharField(max_length=20,null=True)
    categoy = models.ForeignKey(Category, on_delete= models.CASCADE, null=True)
    description = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table="expense"
