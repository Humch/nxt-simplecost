from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class ThirdParty(models.Model):
    
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('expense-list')

class PaymentMode(models.Model):
    
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('expense-list')

class Expense(models.Model):
    
    date_expense = models.DateField()
    third_party = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField(max_length=255,blank=True)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.CASCADE)
    property_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simplecost_owner')
    shared_with = models.ManyToManyField(User, blank=True, related_name='simplecost_user')

    def __str__(self):
        return str(self.date_expense) + '_' + str(self.third_party) + '_' + str(self.amount)
    
    def get_absolute_url(self):
        return reverse('expense-list')
 