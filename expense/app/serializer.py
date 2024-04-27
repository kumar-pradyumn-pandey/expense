from rest_framework import serializers
from app.models import *
class CategoryListSerializer(serializers.ModelSerializer):
    page = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields=['id','name','page',"is_active",'type']
    def get_page(self,obj):
        page = self.context.get('page',1)
        # Access the context from the serializer to get the current index
        counter = self.context.get('counter', 0)
        # Increment the counter for each object
        counter += 1
        # Update the context with the new counter value
        self.context['counter'] = counter
        return (page-1)*10 + counter



class ExpenseListSerializer(serializers.ModelSerializer):
    page = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    class Meta:
        model = Expense
        fields=['id','amount',"category","category__name",'page','category__type','created_on']
    def get_page(self,obj):
        page = self.context.get('page',1)
        # Access the context from the serializer to get the current index
        counter = self.context.get('counter', 0)
        # Increment the counter for each object
        counter += 1
        # Update the context with the new counter value
        self.context['counter'] = counter
        return (page-1)*10 + counter
    def get_created_on(self,obj):
        return obj.created_on.strftime("%d/%m/%Y %I:%M:%S %p")