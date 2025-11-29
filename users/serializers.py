from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, PatientProfile, DoctorProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        default='patient'
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        role = validated_data.get('role', 'patient')
        
        # Используем email как username
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=role
        )
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ('id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class DoctorProfileSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = DoctorProfile
        fields = (
            'id', 'specialization', 'price', 'experience', 
            'bio', 'photo', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserProfileSerializer(serializers.ModelSerializer):
    patient_profile = PatientProfileSerializer(read_only=True)
    doctor_profile = DoctorProfileSerializer(read_only=True)
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'is_active', 'date_joined',
            'patient_profile', 'doctor_profile', 'profile'
        )
        read_only_fields = ('id', 'date_joined', 'is_active')

    def get_profile(self, obj):
        """Возвращает профиль в зависимости от роли пользователя"""
        if obj.role == 'patient' and hasattr(obj, 'patient_profile'):
            return PatientProfileSerializer(obj.patient_profile).data
        elif obj.role == 'doctor' and hasattr(obj, 'doctor_profile'):
            return DoctorProfileSerializer(obj.doctor_profile).data
        return None

