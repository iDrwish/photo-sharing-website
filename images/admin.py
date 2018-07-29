from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created', 'user', 'total_likes']
    list_filter = ['created']


    def get_products(self, obj):
        return "\n".join([p.user_like for p in obj.objects.all()])

admin.site.register(Image, ImageAdmin)