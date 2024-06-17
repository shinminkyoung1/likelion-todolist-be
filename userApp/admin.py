from django.contrib import admin
from .models import User  #.models는 같은 경로에 있는 것을 가져온다는 것 

# Register your models here.
admin.site.register(user)