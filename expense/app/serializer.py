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
    description = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    type= serializers.SerializerMethodField()
    class Meta:
        model = Expense
        fields=['id','amount',"category_id","category_name","type",'page','created_on','description']
    def get_page(self,obj):
        page = self.context.get('page',1)
        # Access the context from the serializer to get the current index
        counter = self.context.get('counter', 0)
        # Increment the counter for each object
        counter += 1
        # Update the context with the new counter value
        self.context['counter'] = counter
        return (page-1)*10 + counter
    def get_description(self,obj):
        if obj.description:
            return obj.description
        else:
            return ""
    def get_category_name(self,obj):
        return obj.category.name
    def get_type(self,obj):
        return obj.category.type
    def get_created_on(self,obj):
        return obj.date.strftime("%d/%m/%Y %I:%M:%S %p")