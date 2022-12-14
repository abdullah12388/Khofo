
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Models
from . import models

# Register your models here.

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Country)
admin.site.register(models.BuyerUserDetails)
