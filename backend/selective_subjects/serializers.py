from rest_framework import serializers
from .models import ElectiveSubjectChoice, CustomUser

class ElectiveSubjectChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectiveSubjectChoice
        fields = ['subject_id', 'subject_name', 'subject_description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'