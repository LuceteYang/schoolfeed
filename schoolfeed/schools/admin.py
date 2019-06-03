from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'image',
        'location',
        'creator',
        'deleted_at',
    )


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'school',
    )


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'school',
        'school',
        'role'
    )


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
