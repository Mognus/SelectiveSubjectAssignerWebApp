from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

router = DefaultRouter()
router.register(r'subjects', views.ElectiveSubjectChoiceViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/get-token/', views.get_token_by_password, name='get_token'),
    path('api/blacklist-token/', views.blacklist_token, name='token_blacklist'),
    path('api/verify-token/', TokenVerifyView.as_view(), name='verify_token'),
]