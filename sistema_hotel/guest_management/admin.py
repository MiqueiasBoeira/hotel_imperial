# guest_management/admin.py

from django.contrib import admin
from .models import Booking, Room, CheckOut, FinancialTransaction

admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(CheckOut)
admin.site.register(FinancialTransaction)



