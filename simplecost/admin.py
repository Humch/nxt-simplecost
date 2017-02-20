from django.contrib import admin

from .models import ThirdParty, PaymentMode, Expense

admin.site.register(ThirdParty)
admin.site.register(PaymentMode)
admin.site.register(Expense)

