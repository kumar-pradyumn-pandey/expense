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

from rest_framework.generics import GenericAPIView
from django.core.paginator import Paginator
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
        category_form=AddCategoryForm()
        context={'form':category_form}
        return render(request,'add_category.html',context)
    def post(self,request):
        category_form=AddCategoryForm(request.POST)
        context={'form':category_form}
        if category_form.is_valid():
            name=category_form.cleaned_data.get('name')
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
            category_instance.save()
            messages.success(request,"Category Added Successfully")
            return render(request,'add_category.html',context)  # type: ignore
        else:
            messages.error(request,'You Entered Wrong data')
            return render(request,'add-category.html',context)  # type: ignore


class CategoryListing(View):
    def get(self, request):
        data = Category.objects.all()
        serializer = CategoryListSerializer(data,many=True)
        return render(request,'category_list.html',context={"category_list":serializer.data})