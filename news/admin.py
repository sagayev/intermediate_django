from django.contrib import admin
from .models import UserProfile, Headline
# Register your models here.
admin.site.register(Headline)
admin.site.register(UserProfile)

