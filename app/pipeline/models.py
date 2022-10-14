from django.db import models


class TestScore(models.Model):
    psychometrics = models.CharField(max_length=10)
    presentation = models.CharField(max_length=10)

    def get_absolute_url(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def get_student_name(self):
        student_information_obj = StudentInformation.objects.get(test_score_id=self.id)
        return student_information_obj.name

    def get_student_absolute_url(self):
        student_information_obj = StudentInformation.objects.get(test_score_id=self.id)
        return student_information_obj.get_absolute_url()


class Invitation(models.Model):
    invited_date = models.DateField(null=True, blank=True)
    invited_by = models.CharField(max_length=200)

    def get_absolute_url(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def get_student_name(self):
        student_information_obj = StudentInformation.objects.get(invitation_id=self.id)
        return student_information_obj.name

    def get_student_absolute_url(self):
        student_information_obj = StudentInformation.objects.get(invitation_id=self.id)
        return student_information_obj.get_absolute_url()


class Trainer(models.Model):
    name = models.CharField(max_length=200)


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def get_all_student_names(self):
        student_information_names = [student.name for student in StudentInformation.objects.filter(course_id=self.id)]
        return student_information_names

    def get_all_student_absolute_urls(self):
        student_information_urls = [student.get_absolute_url() for student in StudentInformation.objects.filter(course_id=self.id)]
        return student_information_urls

    def get_trainer_name(self):
        return self.trainer_id.name


class AcademyPerformance(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    week = models.IntegerField()
    analytic = models.IntegerField(null=True, blank=True)
    independent = models.IntegerField(null=True, blank=True)
    determined = models.IntegerField(null=True, blank=True)
    professional = models.IntegerField(null=True, blank=True)
    studious = models.IntegerField(null=True, blank=True)
    imaginative = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def get_student_name(self):
        student_information_obj = StudentInformation.objects.get(academy_performance_id=self.id)
        return student_information_obj.name

    def get_student_absolute_url(self):
        student_information_obj = StudentInformation.objects.get(academy_performance_id=self.id)
        return student_information_obj.get_absolute_url()


class TechScore(models.Model):
    tech_self_score = models.CharField(max_length=50)
    value = models.IntegerField()


class Strength(models.Model):
    strength = models.CharField(max_length=100)


class Weakness(models.Model):
    weakness = models.CharField(max_length=100)


class TraineePerformance(models.Model):
    self_development = models.BooleanField()
    geo_flex = models.BooleanField()
    financial_support = models.BooleanField()
    course_interest = models.CharField(max_length=500)
    result = models.CharField(max_length=100)
    tech_scores = models.ManyToManyField(TechScore, blank=True)
    strengths = models.ManyToManyField(Strength, blank=True)
    weaknesses = models.ManyToManyField(Weakness, blank=True)

    def get_absolute_url(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def get_student_name(self):
        student_information_obj = StudentInformation.objects.get(trainee_performance_id=self.id)
        return [student_information_obj.name]

    def get_student_absolute_url(self):
        student_information_obj = StudentInformation.objects.get(trainee_performance_id=self.id)
        return student_information_obj.get_absolute_url()


class StudentInformation(models.Model):
    student_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    postcode = models.CharField(max_length=50)
    university = models.CharField(max_length=500, null=True, blank=True)
    degree = models.CharField(max_length=500, null=True, blank=True)
    test_score_id = models.ForeignKey(TestScore, on_delete=models.SET_NULL, null=True, blank=True)  # 1-to-1
    invitation_id = models.ForeignKey(Invitation, on_delete=models.SET_NULL, null=True, blank=True)  # 1-to-1
    academy_performance_id = models.ForeignKey(AcademyPerformance, on_delete=models.SET_NULL, null=True, blank=True)  # 1-to-1
    trainee_performance_id = models.ForeignKey(TraineePerformance, on_delete=models.SET_NULL, null=True, blank=True)  # 1-to-1

    def get_absolute_url(self):
        return self.id
