from rest_framework import serializers
from app.models import *
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=['id','name']