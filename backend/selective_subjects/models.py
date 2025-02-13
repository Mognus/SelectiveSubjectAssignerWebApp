from django.db import models
from django.contrib.auth.models import AbstractUser

class ElectiveSubjectChoice(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=200)
    subject_description = models.TextField()

    def __str__(self):
        return self.subject_name

    class Meta:
        db_table = 'ElectiveSubjectChoice'

class CustomUser(AbstractUser):
    # ID wird automatisch von Django verwaltet
    student_id = models.IntegerField(unique=True)
    first_choice = models.ForeignKey(
        ElectiveSubjectChoice, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='first_choice_users'
    )
    second_choice = models.ForeignKey(
        ElectiveSubjectChoice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='second_choice_users'
    )
    third_choice = models.ForeignKey(
        ElectiveSubjectChoice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='third_choice_users'
    )

    def __str__(self):
        return f"Student {self.student_id}"

    class Meta:
        db_table = 'CustomUser'