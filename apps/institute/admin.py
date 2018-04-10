from django.contrib import admin

from .models import Institute


class InstituteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Institute, InstituteAdmin)
