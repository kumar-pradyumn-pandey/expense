from .views import *
from django.urls import path,include

urlpatterns = [
    path('',LoginPage.as_view(),name=''),
    path('logout',Logout.as_view(),name='logout'),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('category/',CategoryManagement.as_view(),name="category"),
    path('category_list/',CategoryListing.as_view(),name="category_list"),



]