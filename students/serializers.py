import datetime
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# class ItemDescriptionSerializer(serializers.RelatedField):
#     def to_representation(self, value):
#         data = {}
#         for field in ('id', 'locationName', 'locationCountry','Country_code'):
#             data[field] = getattr(value, field)
#         return data

#     def to_internal_value(self, data):
#         return Location.objects.get(id=data)

#     def get_queryset(self, *args):
#         pass


class User_Signup_serilizer(serializers.ModelSerializer):
    # full_name_ = serializers.SerializerMethodField('fullname')
    is_active = serializers.BooleanField(default=True, write_only=True)
    is_staff = serializers.BooleanField(default=False, write_only=True)
    is_superuser = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = User
        
        fields = ("email","first_name","last_name","is_active","is_staff","is_superuser","username","user_type","profile",)
        # read_only_fields = ('full_name_',)
# class ProfileSerilizer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('profile')
    
#     def update(self, instance, validated_data):
#         instance.profile = validated_data.get('profile', instance.profile)
#         instance.save()
#         return instance



class Student_Serilizer(serializers.ModelSerializer):
    full_name_ = serializers.SerializerMethodField('full__name')
    user = User_Signup_serilizer()

    # full_name = User_Signup_serilizer.full_name
    # print(full_name)
    class Meta:
        model = Student
        fields = ("user","roll","date_of_birth","full_name_","is_deleted")
        read_only_fields = ('full_name_',)
        # read_only_fields = ('is_deleted',)

    
    def full__name(self, data):
        fullname = data.user.first_name +" "+ data.user.last_name
        print("This is the data that is generated:",fullname)

        # fullname = data.first_name + data.last_name
        return fullname
    
class PostStudentSerilizer(serializers.ModelSerializer):
    
# full_name = User_Signup_serilizer.full_name
    # print(full_name)
    is_deleted = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = Student
        fields = ("user","roll","date_of_birth","is_deleted")

class PostTeacherSerilizer(serializers.ModelSerializer):
    
# full_name = User_Signup_serilizer.full_name
    # print(full_name)
    is_deleted = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = Teacher
        fields = ("user","date_of_birth","subject_name","is_deleted",)

class Teacher_Serilizer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('full__name')
    # user = User_Signup_serilizer()
    class Meta:
        model = Teacher
        fields = ("user","date_of_birth","subject_name","full_name",)
        

    def full__name(self, data):
        fullname = data.user.first_name +" "+ data.user.last_name
        print("This is the data that is generated:",fullname)

        # fullname = data.first_name + data.last_name
        return fullname


class Subjects_Serilizer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields =("name","faculty",)


class PostSubjectsSerilizer(serializers.ModelSerializer):
    is_deleted = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = Subjects
        fields =("name","faculty","is_deleted",)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['username'] = self.user.username
        data['is_superuser'] = self.user.is_superuser
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token




class DashboardSerilizer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('name')
    user_details = serializers.SerializerMethodField('student_or_teacher')
    # student = Student_Serilizer()
    # teacher = Teacher_Serilizer()

    class Meta:
        model = User
        fields =("email","full_name","user_details",)
        read_only_fields = ('full_name','user_details',)


    
    def name(self, data):
        fullname = data.first_name +" "+ data.last_name
        print("This is the data that is generated:",fullname)
        # fullname = data.first_name + data.last_name
        return fullname
    def student_or_teacher(self,data):
        if data.user_type == "Teacher":
            
            teacher = Teacher.objects.filter(user_id=data.id ,is_deleted=False).last()
            data_field = Teacher_Serilizer(instance=teacher)
            return data_field.data
        elif data.user_type == "Student":
            student = Student.objects.filter(user_id=data.id ,is_deleted=False).last()
            data_field = Student_Serilizer(instance=student)
            return data_field.data
        else:
            data_field = Subjects_Serilizer()         
            return data_field.data   



    


