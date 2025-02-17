from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ElectiveSubjectChoice

class CustomUserAdmin(UserAdmin):
    # Felder die in der Liste angezeigt werden
    list_display = ('username', 'email', 'student_id', 'first_name', 'last_name', 'is_staff')
    
    # Felder für die Suche
    search_fields = ('username', 'student_id', 'email', 'first_name', 'last_name')
    
    # Felder für die Filterleiste
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    # Feldsets für das Bearbeitungsformular
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'student_id')}),
        ('Subject Choices', {'fields': ('first_choice', 'second_choice', 'third_choice')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Feldsets für das Erstellungsformular
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'student_id'),
        }),
    )

# Registriere die Models für das Admin Interface
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ElectiveSubjectChoice)