from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Users)
admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.Marks)