from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Contents)
class Contentsdmin(admin.ModelAdmin):
    list_display = (
    	'id',
        'school',
        'creator',
        'main_image',
        'text',
        'deleted_at',
    )
