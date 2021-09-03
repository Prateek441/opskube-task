from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Userprofile)
admin.site.register(BookDetail)
admin.site.register(Book_sold)
admin.site.register(Cart)
admin.site.register(Orders)