from django.db import models


class TestScore(models.Model):
    psychometrics = models.CharField(max_length=10)
    presentation = models.CharField(max_length=10)


class Invitation(models.Model):
    date = models.DateField(null=True, blank=True)
    invited_by = models.CharField(max_length=200)


class Trainer(models.Model):
    name = models.CharField(max_length=200)


class Course(models.Model):
    week = models.IntegerField()
    course_name = models.CharField(max_length=200)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return self.id


class AcademyPerformance(models.Model):
    week = models.IntegerField()
    analytic = models.IntegerField(null=True, blank=True)
    independent = models.IntegerField(null=True, blank=True)
    determined = models.IntegerField(null=True, blank=True)
    professional = models.IntegerField(null=True, blank=True)
    studious = models.IntegerField(null=True, blank=True)
    imaginative = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['week', 'student_information_id']

    def get_absolute_url(self):
        return self.id


class TechScore(models.Model):
    tech_score_name = models.CharField(max_length=50)
    value = models.IntegerField()


class Strength(models.Model):
    strength = models.CharField(max_length=100)


class Weakness(models.Model):
    weakness = models.CharField(max_length=100)


class TraineePerformance(models.Model):
    student_information_id = models.ForeignKey('StudentInformation', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    self_development = models.BooleanField()
    geo_flex = models.BooleanField()
    financial_support = models.BooleanField()
    course_interest = models.CharField(max_length=500)
    tech_scores = models.ManyToManyField(TechScore, blank=True)
    strengths = models.ManyToManyField(Strength, blank=True)
    weaknesses = models.ManyToManyField(Weakness, blank=True)

    def get_absolute_url(self):
        return self.id


class StudentInformation(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    postcode = models.CharField(max_length=50)
    university = models.CharField(max_length=500, null=True, blank=True)
    degree = models.CharField(max_length=500, null=True, blank=True)
    test_score_id = models.ForeignKey(TestScore, on_delete=models.SET_NULL, null=True, blank=True)
    invitation_id = models.ForeignKey(Invitation, on_delete=models.SET_NULL, null=True, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    academy_performance_id = models.ForeignKey(AcademyPerformance, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return self.id
