from rest_framework import serializers
from .models import Expense, Income


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'description', 'date']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'source', 'amount', 'description', 'date']
