from django.contrib import admin
from .models import User 
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email',) #튜플형태 

admin.site.register(User, UserAdmin) #등록