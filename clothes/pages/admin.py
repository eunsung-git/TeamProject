from django.contrib import admin
from .models import Category, Closet, Profile

# class CategoryAdmin(admin.ModelAdmin):
# 	list_display = ('pk','title','created_at','updated_at',)


# class ClosetAdmin(admin.ModelAdmin):
# 	list_display = (')

# class ProfileAdmin(admin.ModelAdmin):
# 	list_display = ()

admin.site.register(Category)
admin.site.register(Closet)
admin.site.register(Profile)