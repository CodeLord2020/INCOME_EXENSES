from django.db import models
from authentication.models import User

# Create your models here.
cat_options = [
    ('Gadgets', 'Gadgets'),
     ('Books', 'Books'),
      ('Home', 'Home'),
       ('Internet', 'Internet'),
        ('Transport', 'Transport'),
         ('Food', 'Food'),
          ('Others', 'Others'),
]

income_cat_options = [

       ('Salary', 'Salary'),
        ('Allowance', 'Allowance'),
         ('Hustle', 'Hustle'),
          ('Ritual', 'Ritual'),
           ('Others', 'Others'),
]

class Expense(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices= cat_options)
    amount = models.DecimalField(max_digits=10, decimal_places=2,max_length=220)
    description = models.TextField()
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner)+"'s Expenses."



class Income(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=10, choices= income_cat_options)
    amount = models.DecimalField(max_digits=10, decimal_places=2,max_length=220)
    description = models.TextField()
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner)+"'s Incomes."