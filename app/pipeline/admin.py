from django.contrib import admin
from .models import TestModel

#############################
#  TEST MODEL REMOVE LATER  #
#############################


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    pass
