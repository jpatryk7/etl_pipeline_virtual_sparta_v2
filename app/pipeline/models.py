from django.db import models


class TestScore(models.Model):
    psychometrics = models.CharField()
    presentation = models.CharField()


class Invitation(models.Model):
    date = models.DateField(null=True, blank=True)
    invited_by = models.CharField()


class Trainer(models.Model):
    name = models.CharField()


class Course(models.Model):
    week = models.IntegerField()
    course_name = models.CharField()
    trainer_id = models.ForeignKey(Trainer, on_delete=models.SET_NULL)


class AcademyPerformance(models.Model):
    week = models.IntegerField()
    student_information_id = models.ForeignKey('StudentInformation', on_delete=models.SET_NULL)
    analytic = models.IntegerField(null=True, blank=True)
    independent = models.IntegerField(null=True, blank=True)
    determined = models.IntegerField(null=True, blank=True)
    professional = models.IntegerField(null=True, blank=True)
    studious = models.IntegerField(null=True, blank=True)
    imaginative = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['week', 'student_information_id']


class TechScore(models.Model):
    tech_score_name = models.CharField()
    value = models.IntegerField()


class Strength(models.Model):
    strength = models.CharField()


class Weakness(models.Model):
    weakness = models.CharField()


class TraineePerformance(models.Model):
    student_information_id = models.ForeignKey('StudentInformation', on_delete=models.SET_NULL)
    date = models.DateField()
    self_development = models.BooleanField()
    geo_flex = models.BooleanField()
    financial_support = models.BooleanField()
    course_interest = models.CharField()
    tech_scores = models.ManyToManyField(TechScore, null=True, blank=True)
    strengths = models.ManyToManyField(Strength, null=True, blank=True)
    weaknesses = models.ManyToManyField(Weakness, null=True, blank=True)


class StudentInformation(models.Model):
    name = models.CharField()
    gender = models.CharField()
    dob = models.DateField()
    email = models.CharField()
    city = models.CharField()
    address = models.CharField()
    postcode = models.CharField()
    university = models.CharField(null=True, blank=True)
    degree = models.CharField(null=True, blank=True)
    test_score_id = models.ForeignKey(TestScore, on_delete=models.SET_NULL, null=True, blank=True)
    invitation_id = models.ForeignKey(Invitation, on_delete=models.SET_NULL, null=True, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    academy_performance_id = models.ForeignKey(AcademyPerformance, on_delete=models.SET_NULL, null=True, blank=True)
