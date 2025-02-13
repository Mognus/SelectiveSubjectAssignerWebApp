from rest_framework import viewsets
from .models import ElectiveSubjectChoice, CustomUser
from .serializers import ElectiveSubjectChoiceSerializer, UserSerializer

class ElectiveSubjectChoiceViewSet(viewsets.ModelViewSet):
    queryset = ElectiveSubjectChoice.objects.all()
    serializer_class = ElectiveSubjectChoiceSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer