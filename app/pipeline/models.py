from django.db import models

#############################
#  TEST MODEL REMOVE LATER  #
#############################


class TestModel(models.Model):
    field_one = models.TextField(max_length=1000)
    field_two = models.CharField(max_length=100)
    field_three = models.IntegerField()

    def get_absolute_url(self):
        return self.id
