from django.contrib import admin
from .models import *


@admin.register(TestScore)
class TestScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(AcademyPerformance)
class AcademyPerformanceAdmin(admin.ModelAdmin):
    pass


@admin.register(TechScore)
class TechScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Strength)
class StrengthAdmin(admin.ModelAdmin):
    pass


@admin.register(Weakness)
class WeaknessAdmin(admin.ModelAdmin):
    pass


@admin.register(TraineePerformance)
class TraineePerformanceAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentInformation)
class StudentInformationAdmin(admin.ModelAdmin):
    pass
