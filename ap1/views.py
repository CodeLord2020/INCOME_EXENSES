from django.shortcuts import render
from rest_framework import generics, views
from .serializers import ExpenseSerializer, IncomeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Expense, Income
from .permissionss import IsOwner
# Create your views here.

class ExpenseListView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
    

class ExpenseLDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
    
    

class IncomeListView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
    

class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)