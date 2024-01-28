from .views import *
from django.urls import path,include

urlpatterns = [
    path('',LoginPage.as_view(),name=''),
    path('logout',Logout.as_view(),name='logout'),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),

]