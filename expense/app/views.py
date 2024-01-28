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