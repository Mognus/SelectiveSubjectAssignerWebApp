from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import ElectiveSubjectChoice, CustomUser
from .serializers import ElectiveSubjectChoiceSerializer, UserSerializer

class ElectiveSubjectChoiceViewSet(viewsets.ModelViewSet):
    queryset = ElectiveSubjectChoice.objects.all()
    serializer_class = ElectiveSubjectChoiceSerializer
    permission_classes = [IsAdminUser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]