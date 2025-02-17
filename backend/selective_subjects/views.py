from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import ElectiveSubjectChoice, CustomUser
from .serializers import ElectiveSubjectChoiceSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class ElectiveSubjectChoiceViewSet(viewsets.ModelViewSet):
    queryset = ElectiveSubjectChoice.objects.all()
    serializer_class = ElectiveSubjectChoiceSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  # Füge diese Zeile hinzu
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_by_password(request):
    password = request.data.get('password')
    
    if not password:
        return Response({
            'error': 'Password is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    User = get_user_model()
    found_user = None
    
    for user in User.objects.all():
        if user.check_password(password):
            found_user = user
            break
    
    if found_user:
        refresh = RefreshToken.for_user(found_user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': found_user.id,
            'student_id': found_user.student_id
        })
    
    return Response({
        'error': 'Invalid password'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def blacklist_token(request):
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Token dekodieren
        token_obj = AccessToken(token)
        
        # OutstandingToken erstellen, falls nicht vorhanden
        outstanding_token, _ = OutstandingToken.objects.get_or_create(
            jti=token_obj['jti'],
            defaults={
                'token': token,
                'created_at': token_obj.current_time,
                'expires_at': token_obj.current_time + token_obj.lifetime,
                'user_id': token_obj['user_id']
            }
        )
        
        # Token zur Blacklist hinzufügen
        BlacklistedToken.objects.get_or_create(token=outstanding_token)
        
        return Response({
            'status': 'Token blacklisted'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)