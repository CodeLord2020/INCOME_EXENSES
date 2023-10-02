from django.urls import path
from . import views


urlpatterns= [
    path('expense/', views.ExpenseListView.as_view(), name = 'expense_list'),
    path('expense_detail/<int:id>', views.ExpenseLDetailView.as_view(), name = 'expense_detail'),

    path('income/', views.IncomeListView.as_view(), name = 'Income_list'),
    path('Income_detail/<int:id>/', views.IncomeDetailView.as_view(), name = 'Income_detail'),



]