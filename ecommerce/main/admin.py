from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Payment)