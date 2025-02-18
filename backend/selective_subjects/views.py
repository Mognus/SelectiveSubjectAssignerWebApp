import json, os
from django.conf import settings
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
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def import_data(request):
    try:
        # read JSON-File
        json_path = os.path.join(settings.BASE_DIR, 'StudentData.json')
        with open(json_path, 'r') as file:
            data = json.load(file)

        # Check for existing student IDs first
        User = get_user_model()
        student_ids = [str(student['studentId']) for student in data['studentList']]
        existing_students = User.objects.filter(student_id__in=student_ids)
        
        if existing_students.exists():
            existing_ids = [str(student.student_id) for student in existing_students]
            return Response({
                'error': 'Import aborted. Following student IDs already exist',
                'existing_ids': existing_ids
            }, status=status.HTTP_409_CONFLICT)

        # If no existing students found, proceed with import
        # create Subjects
        created_subjects = []
        for subject in data['subjectList']:
            subject_obj, created = ElectiveSubjectChoice.objects.get_or_create(
                subject_name=subject['subjectName'],
                defaults={
                    'subject_description': subject['subjectDescription']
                }
            )
            created_subjects.append(subject_obj)

        # create Users
        created_users = []
        for student in data['studentList']:
            username = str(student['studentId'])
            
            user = User.objects.create_user(
                username=username,
                student_id=student['studentId'],
                is_active=True,
                password=student['OTP']
            )
            created_users.append(username)

        return Response({
            'message': 'Data initialized successfully',
            'subjects_created': len(created_subjects),
            'users_created': len(created_users)
        }, status=status.HTTP_201_CREATED)

    except FileNotFoundError:
        return Response({
            'error': 'StudentData.json not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON format'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def export_data(request):
    try:
        # get all subjects
        subjects = ElectiveSubjectChoice.objects.all()
        subject_list = [
            {
                "subjectId": subject.subject_id,
                "subjectName": subject.subject_name,
                "subjectDescription": subject.subject_description
            }
            for subject in subjects
        ]

        # get all non-admin Users 
        students = CustomUser.objects.filter(is_superuser=False)
        student_list = []
        
        for student in students:
            student_data = {
                "studentId": str(student.student_id),  
            }
            
            # only add choices if they exist
            if student.first_choice:
                student_data["firstChoice"] = student.first_choice.subject_id
            else:
                student_data["firstChoice"] = None
                
            if student.second_choice:
                student_data["secondChoice"] = student.second_choice.subject_id
            else:
                student_data["secondChoice"] = None
                
            if student.third_choice:
                student_data["thirdChoice"] = student.third_choice.subject_id
            else:
                student_data["thirdChoice"] = None
                
            student_list.append(student_data)

        # create export dictionary
        export_data = {
            "subjectList": subject_list,
            "studentList": student_list
        }

        # Safe Data in Json-File
        export_path = os.path.join(settings.BASE_DIR, 'StudentExport.json')
        with open(export_path, 'w', encoding='utf-8') as file:
            json.dump(export_data, file, indent=2, ensure_ascii=False)

        return Response({
            'message': 'Data exported successfully',
            'file_path': export_path,
            'subjects_exported': len(subject_list),
            'students_exported': len(student_list)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)