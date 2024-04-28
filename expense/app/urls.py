from .views import *
from django.urls import path,include

urlpatterns = [
    path('',LoginPage.as_view(),name=''),
    path('logout',Logout.as_view(),name='logout'),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('category/',CategoryManagement.as_view(),name="category"),
    path('category_list/',CategoryListing.as_view(),name="category_list"),
    path('active_inactive_category/<int:id>/',ActiveInactiveCategory.as_view(),name="active_inactive_category"),
    path('delete_category/<int:id>/',DeleteCategory.as_view(),name="delete_category"),
    path('edit_category/<int:id>/',EditCategoryGet.as_view(),name="edit_category"),
    path('update_category/',EditCategoryUpdate.as_view(),name="update_category"),


    path("expense_list/",ListAllExpenses.as_view(),name="expense_list"),
    path("expense/",ExpenseManagement.as_view(),name="expense"),
    path("delete_expense/<int:id>",DeleteExpense.as_view(),name="delete_expense")







]