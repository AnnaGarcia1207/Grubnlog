from django.contrib import admin
from .models import Food, Profile, Diet, Log


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Food)
admin.site.register(Profile)
admin.site.register(Diet)
admin.site.register(Log)
