from rest_framework import serializers
from .models import ElectiveSubjectChoice, CustomUser

class ElectiveSubjectChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectiveSubjectChoice
        fields = ['subject_id', 'subject_name', 'subject_description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'student_id', 'username', 'first_choice', 
                 'second_choice', 'third_choice']