from itertools import product
from django.shortcuts import render
import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse  # type: ignore
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.views import APIView
from .forms import *
from rest_framework.response import Response
from django.views import View
from django.contrib import messages
from .UserBackendAuthenticate import CustomBackendAuthenticate
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from .serializer import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.generics import GenericAPIView
import time
class LoginPage(View):
    form_class = LoginForm

    def get(self, request):
        login_form = self.form_class
        context = {'form': login_form}
        return render(request, 'login.html', context)

    def post(self, request):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            email_or_phone = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = CustomBackendAuthenticate.authenticate(
                request, username=email_or_phone, password=password)
            if user:
                login(request, user, backend='app.UserBackendAuthenticate.CustomBackendAuthenticate')
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, 'User Not Found')
                return render(request, 'login.html', {'form': login_form})

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse(''))
class Dashboard(View):

    def get(self, request):
        user = request.user
        context = {'data': {"user":user}}
        return render(request, 'dashboard.html', context)


class CategoryManagement(View):
    def get(self, request):
        user = request.user
        category_form=AddCategoryForm()
        context={'form':category_form,"data":{"user":user}}
        return render(request,'add_category.html',context)
    def post(self,request):
        category_form=AddCategoryForm(request.POST)
        context={'form':category_form}
        if category_form.is_valid():
            name=category_form.cleaned_data.get('name')
            type=category_form.cleaned_data.get('type')

            # image = category_form.cleaned_data.get('image')
            # image_list = request.FILES.getlist('image')
            # fs = FileSystemStorage("media/media/")
            # filename = fs.save(image.name, image)
            # image_url = fs.url(filename)
            check_existing_category = Category.objects.filter(name__iexact = name)
            if check_existing_category:
                messages.error(request,"Category Already Exists!")
                return render(request,'add_category.html',context)
            category_instance=Category(name=name)
            category_instance.type = type
            category_instance.save()
            messages.success(request,"Category Added Successfully")
            return render(request,'add_category.html',context)  # type: ignore
        else:
            messages.error(request,'You Entered Wrong data')
            return render(request,'add-category.html',context)  # type: ignore


class CategoryListing(View):
    def get(self, request):
        user = request.user
        data = Category.objects.all().order_by('-created_on')
        serializer = CategoryListSerializer(data,many=True)
        data = serializer.data
        paginator = Paginator(data,5)  # Show 10 objects per page
        page = request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objects = paginator.page(1)
            page=1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objects = paginator.page(paginator.num_pages)
        return render(request,'category_list.html',context={"category_list":objects,"page":page,"counter":0,"data":{"user":user}})

class ActiveInactiveCategory(View):
    def get(self,request,id):
        category = Category.objects.filter(id = int(id)).last()
        if category.is_active:
            category.is_active = False
        else:
            category.is_active = True
        category.save()
        return redirect(reverse("category_list"))

class DeleteCategory(View):
    def get(self,request,id):
        category = Category.objects.filter(id = int(id)).last()
        category.delete()
        return redirect(reverse("category_list"))


class EditCategoryGet(View):
    def get(self,request,id):
        # storage = messages.get_messages(request)
        # for message in storage:
        #     if message.level == messages.SUCCESS:
        #         del storage._loaded_messages[0]
        data = Category.objects.filter(id = int(id)).last()
        editForm = EditCategoryForm(instance=data)
        # editForm.fields['name'].queryset = data.name
        context = {'data': data,"form":editForm}
        return render(request, 'edit_category.html', context)
class EditCategoryUpdate(View):
    def post(self,request):
        category_form=EditCategoryForm(request.POST)
        context={'form':category_form}
        if category_form.is_valid():
            name=category_form.cleaned_data.get('name')
            type=category_form.cleaned_data.get('type')

            check_existing_category = Category.objects.filter(name__iexact = name).last()
            id=category_form.cleaned_data.get('id')
            if check_existing_category:
                if check_existing_category.id != category_form.cleaned_data.get('id'):
                    messages.error(request,"Category Already Exists!")
                    data = Category.objects.filter(id = int(id)).last()
                    editForm = EditCategoryForm(instance=data)
                    # editForm.fields['name'].queryset = data.name
                    context = {'data': data,"form":editForm}
                    return render(request, 'edit_category.html', context)
            cat_data = Category.objects.filter(id =category_form.cleaned_data.get('id')).last()
            cat_data.name=name
            cat_data.type = type
            cat_data.save()
            messages.success(request,"Category Updated Successfully")
            data = Category.objects.filter(id = int(id)).last()
            editForm = EditCategoryForm(instance=data)
            # editForm.fields['name'].queryset = data.name
            context = {'data': data,"form":editForm}
            return render(request, 'edit_category.html', context)
        else:
            messages.error(request,"You Entered Wrong Data!")
            data = Category.objects.filter(id = int(id)).last()
            editForm = EditCategoryForm(instance=data)
            # editForm.fields['name'].queryset = data.name
            context = {'data': data,"form":editForm}
            return render(request, 'edit_category.html', context)


class ListAllExpenses(View):
    def get(self,request):
        user = request.user
        data = Expense.objects.all().order_by('-created_on')
        serializer = ExpenseListSerializer(data,many=True)
        data = serializer.data
        paginator = Paginator(data,15)  # Show 15 objects per page
        page = request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objects = paginator.page(1)
            page=1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objects = paginator.page(paginator.num_pages)
        return render(request,'expense_list.html',context={"expense_list":objects,"page":page,"counter":0,"data":{"user":user}})