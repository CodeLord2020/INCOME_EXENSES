from django.shortcuts import render
from rest_framework import generics
from ap1.models import Expense
import datetime

# Create your views here.

class ExpenseStats(generics.GenericAPIView):

    def get(self, request):
        today_date = datetime.date.today
        a_year_ago = today_date - datetime.timedelta(days=365)
        expenses = Expense.objects.filter(owner = request.user,
                                          date__gte = a_year_ago,
                                          date__lte = today_date )
        final = { }
