import datetime
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *


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
        
        fields = ("email","first_name","last_name","is_active","is_staff","is_superuser","username","user_type",)
        # read_only_fields = ('full_name_',)


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
    is_deleted = serializers.BooleanField(default=True, write_only=True)
    class Meta:
        model = Student
        fields = ("user","roll","date_of_birth","is_deleted")


class Teacher_Serilizer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("name_ID","date_of_birth","subject_ID",)


class Subjects_Serilizer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields =("name","faculty",)




# class User_Login_serilizer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username","password",)
