from django.contrib import admin

from .models import UserProfile


class UserProdileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'default_email'
    )

    ordering = ('user',)


admin.site.register(UserProfile, UserProdileAdmin)