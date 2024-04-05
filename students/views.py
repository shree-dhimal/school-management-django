from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
# from .models import Item,Location, Bike
from rest_framework import generics
from rest_framework.views import APIView, status
from .serializers import *
from .models import *
# from .utility import validate_if_id_exist
# import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.parsers import (MultiPartParser,FormParser)
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.mail import EmailMessage

#user Signup
class UserSignupView(APIView):
    # def get(self,request):
    #     queryset = User.objects.all().values()
    #     print(queryset)

    #     return Response(queryset,status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        image = request.FILES.get('image')
        data.update({"profile": image})
        # print(image)
        try:
            serilizer = User_Signup_serilizer(data=data)
            # print(serilizer.initial_data)
            if serilizer.is_valid():
                if data['password']:
                    # print("I am HEre")
                    user = serilizer.save()
                    user.set_password(data['password'])
                    user.save()
                    subject ="Sucessfully Registered"
                    message =" Thank you for joining us"
                    to_email = request.data['email']
                    l = []
                    l.append(to_email)
                    print(l)
                    try:
                        send_email(subject,message,l)
                    except Exception as e:
                        print(e)
                        
                    # print("This is the user that is saved",user)
                    # print(serilizer.data)
                    return Response({"message": serilizer.data},status.HTTP_200_OK)
                else:
                    return Response({"message": "Please Enter a Vaild Password"},status.HTTP_200_OK)

            else:
                return Response({"message": serilizer.errors},status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR)



class Student_Details(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        print(request.user)
        data = request.user.user_type
        user_id = request.user.id
        print(user_id)

        student = Student.objects.filter(user_id=user_id, is_deleted=False)

        # print("This is the student fettched",student.last().is_deleted)
        if student.last() is not None:
            serilizer = Student_Serilizer(student.last())
            print(serilizer.data)
            # print(student.is_deleted)
            if data == "Student":
                return Response(serilizer.data,status.HTTP_200_OK)
            else:
                message= {"Message":"You are not Student"}
                return Response(message,status.HTTP_400_BAD_REQUEST)
        else:
            message= {"Message":f"You have not populated the Sudent Data, please put some Data first {request.user.first_name}"}
            return Response(message,status.HTTP_400_BAD_REQUEST)

        
    def post(self, request):
        data = request.data
        user_id = request.user.id
        print(user_id)
        student = Student.objects.filter(user_id=user_id, is_deleted=False).last()
        user_type = request.user.user_type
        data.update({"user": user_id})
        print("This is what student returns:",student)
        # print(user_type)
        # print(serilizer.initial_data)
        # print("This is the data that is got from the login user ",user_id)
        if user_type == "Student":
            if student is None:
                serilizer = PostStudentSerilizer(data=data)
                if serilizer.is_valid():
                    # print("ima herere")
                    serilizer.save()
                    # message= {"Message":"Im here"}
                    message= {"Data":serilizer.data,"Message":"Sucessfull"}
                    return Response(message,status.HTTP_201_CREATED)
                else:
                    return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)
            else:

                message= {"Message":"The Logged in user has data already"}
                return Response(message,status.HTTP_400_BAD_REQUEST) 
        else:
            message= {"Message":"The Logged in user is not Student"}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request):
        data = request.data
        user_id = request.user.id
        print(user_id)
        student = Student.objects.filter(user_id=user_id, is_deleted=False).last()
        user_type = request.user.user_type
        data.update({"user": user_id})
        print("This is what student returns:",student)
        # print(user_type)
        # print(serilizer.initial_data)
        # print("This is the data that is got from the login user ",user_id)
        if user_type == "Student":
            if student is not None:
                serilizer = PostStudentSerilizer(instance=student,data=data)
                if serilizer.is_valid():
                    # print("ima herere")
                    serilizer.save()
                    # message= {"Message":"Im here"}
                    message= {"Data":serilizer.data,"Message":"Data Updated Sucessfull"}
                    return Response(message,status.HTTP_201_CREATED)
                else:
                    return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)
            else:

                message= {"Message":"The Logged in user has no data to update"}
                return Response(message,status.HTTP_400_BAD_REQUEST) 
        else:
            message= {"Message":"The Logged in user is not Student"}
    
    def delete(self, request):
        # data = data.is_deleted[True]
        user_id = request.user.id
        # print(user_id)

        student = Student.objects.filter(user_id=user_id, is_deleted=False).last()
        # print(student.last())
        if student:
            student.is_deleted = True
            student.save()

            res = {"Data":"student","Message":"The Item is deleted"}
            return Response(res, status.HTTP_200_OK)
            # else:
            #     res = {"Data":"Error","Message":"The users is already deleted"}
            #     return Response(res, status.HTTP_200_OK)
        else:
            res = {"Data":"Error","Message":"Users Student Details not Foundd to Delete"}

            return Response(res, status.HTTP_400_BAD_REQUEST)

        
class Teacher_Details(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        print(request.user)
        user_id = request.user.id
        print(user_id)
        is_deleted = Teacher.objects.filter(user_id=user_id).values('is_deleted')
        print(is_deleted)
        data = request.user.user_type
        teacher = Teacher.objects.filter(user_id=user_id, is_deleted=False).last()
        # print("This is the student fettched",student.last().is_deleted)
        if teacher is not None:
            serilizer = Teacher_Serilizer(teacher)
            print(serilizer.data)
            # print(student.is_deleted)
            if data == "Teacher":
                return Response(serilizer.data,status.HTTP_200_OK)
            else:
                message= {"Message":"You are not Teacher"}
                return Response(message,status.HTTP_400_BAD_REQUEST)
        else:
            message= {"Message":f"There is no data, please put some Data first {request.user.first_name}"}
            return Response(message,status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        data = request.data
        user_id = request.user.id
        print(user_id)
        teacher = Teacher.objects.filter(user_id=user_id, is_deleted=False).last()
        user_type = request.user.user_type
        data.update({"user": user_id})
        serilizer = PostTeacherSerilizer(data=data)

        print("This is what student returns:",teacher)
        # print(user_type)
        print(serilizer.initial_data)
        # print("This is the data that is got from the login user ",user_id)
        if user_type == "Teacher":
            if teacher is None:
                if serilizer.is_valid():
                    # print("ima herere")
                    serilizer.save()
                    # message= {"Message":"Im here"}
                    message= {"Data":serilizer.data,"Message":"Sucessfull"}
                    return Response(message,status.HTTP_201_CREATED)
                else:
                    return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)
            message= {"Message":"The Logged in user has data already"}
            return Response(message,status.HTTP_400_BAD_REQUEST) 
        else:
            message= {"Message":"The Logged in user is not Teacher"}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        

    def put(self, request):
        data = request.data
        user_id = request.user.id
        print(user_id)
        teacher = Teacher.objects.filter(user_id=user_id, is_deleted=False).last()
        user_type = request.user.user_type
        data.update({"user": user_id})
        print("This is what student returns:",teacher)
        # print(user_type)
        # print(serilizer.initial_data)
        # print("This is the data that is got from the login user ",user_id)
        if user_type == "Teacher":
            if teacher is not None:
                serilizer = PostStudentSerilizer(instance=teacher,data=data)
                if serilizer.is_valid():
                    # print("ima herere")
                    serilizer.save()
                    # message= {"Message":"Im here"}
                    message= {"Data":serilizer.data,"Message":"Data Updated Sucessfull"}
                    return Response(message,status.HTTP_201_CREATED)
                else:
                    return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)
            else:

                message= {"Message":"The Logged in user has no data to update"}
                return Response(message,status.HTTP_400_BAD_REQUEST) 
        else:
            message= {"Message":"The Logged in user is not Teacher"}
        
        
    
    def delete(self, request):
        # data = data.is_deleted[True]
        user_id = request.user.id
        # print(user_id)

        teacher = Teacher.objects.filter(user_id=user_id, is_deleted=False).last()
        # print(student.last())
        if teacher:
            teacher.is_deleted = True
            teacher.save()

            res = {"Data":"teacher","Message":"The Item is deleted"}
            return Response(res, status.HTTP_200_OK)
            # else:
            #     res = {"Data":"Error","Message":"The users is already deleted"}
            #     return Response(res, status.HTTP_200_OK)
        else:
            res = {"Data":"Error","Message":"Users Student Details not Foundd to Delete"}

            return Response(res, status.HTTP_400_BAD_REQUEST)


class Subject_Details(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        print(request.user)
        user_id = request.user.id
        print(user_id)
        user_type = request.user.user_type
        subject = Subjects.objects.filter(is_deleted=False)
        # mydata = Member.objects.
        # print("this is the subject details", )
        print("This is the student fettched",subject)
        if subject :
            print("I am inside here")
            serilizer = Subjects_Serilizer(subject,many =True)
            print(serilizer.data)
            # print(student.is_deleted)
            if user_type == "Management" or user_type == "Teacher" or user_type == "Student":
                return Response(serilizer.data,status.HTTP_200_OK)
            else:
                message= {"Message":"Not Authorized to view"}
                return Response(message,status.HTTP_400_BAD_REQUEST)
        else:
            message= {"Message":f"There is no data in the Subjects {request.user.first_name}"}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        data = request.data
        user_id = request.user.id
        print(user_id)
        subject_name = Subjects.objects.filter(name=data['name'], is_deleted = False).last()
        faculty = Subjects.objects.filter(faculty=data['faculty']).last()
        user_type = request.user.user_type
        # data.update({"user": user_id})
        serilizer = PostSubjectsSerilizer(data=data)

        print("This is what student returns:",subject_name)
        # print(user_type)
        print(serilizer.initial_data)
        # print("This is the data that is got from the login user ",user_id)
        if user_type == "Management":
            if subject_name is None:
                if serilizer.is_valid():
                    # print("ima herere")
                    serilizer.save()
                    # message= {"Message":"Im here"}
                    message= {"Data":serilizer.data,"Message":"Sucessfull Added the Subjects"}
                    return Response(message,status.HTTP_201_CREATED)
                else:
                    return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)
            else:
                message= {"Data":"Error","Message":"Subjects ALready Exist"}
                return Response(message,status.HTTP_400_BAD_REQUEST)


        else:
            message= {"Message":"The Logged in user is not Managment"}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
    def put(self, request,id):
        data = request.data
        # user_id = request.user.id
        # print(user_id)
        subject = Subjects.objects.filter(id=id, is_deleted=False).last()
        user_type = request.user.user_type
        # data.update({"user": user_id})
        print("This is what subject returns:",subject)
        # print(user_type)
        # print(serilizer.initial_data)
        # print("This is the data that is got from the login user ",user_id)
        if user_type == "Management":
            if subject is not None:
                serilizer = PostStudentSerilizer(instance=subject,data=data)
                if serilizer.is_valid():
                    # print("ima herere")
                    serilizer.save()
                    # message= {"Message":"Im here"}
                    message= {"Data":serilizer.data,"Message":"Data Updated Sucessfull"}
                    return Response(message,status.HTTP_201_CREATED)
                else:
                    return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)
            else:

                message= {"Message":"There is no subject data to update"}
                return Response(message,status.HTTP_400_BAD_REQUEST) 
        else:
            message= {"Message":"The Logged in user is not Management"}

    def delete(self, request, id):
        # data = data.is_deleted[True]
        # user_id = request.user.id
        # print(user_id)

        subject = Subjects.objects.filter(id= id,is_deleted=False).last()
        # print(student.last())
        if subject:
            subject.is_deleted = True
            subject.save()

            res = {"Data":"subject","Message":"The Subject is deleted"}
            return Response(res, status.HTTP_200_OK)
            # else:
            #     res = {"Data":"Error","Message":"The users is already deleted"}
            #     return Response(res, status.HTTP_200_OK)
        else:
            res = {"Data":"Error","Message":"Subject Details not Foundd to Delete"}

            return Response(res, status.HTTP_400_BAD_REQUEST)



def send_email(subject,message,to_email):
    print("I am here")
    print(subject,message,to_email)
    if subject and message and to_email:
        print("I am here")

        try:
            # send(subject, message, to_email):
            send_mail(subject, message,settings.EMAIL_HOST_USER,to_email)

            print("sucess")

        except BadHeaderError as e:
            print(e)
        # return HttpResponseRedirect("/contact/thanks/")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        print("No vaild email")
        pass

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        print(request.user)
        user_id = request.user.id
        user_type = request.user.user_type
        print(user_id)

        user = User.objects.filter(id=user_id ,is_deleted=False).last()
        user1 = User.objects.filter(id=user_id ,is_deleted=False).last()
        print(user1)
        if user1 is not None:
            serilizer = DashboardSerilizer(instance=user1)
            # if serilizer.is_valid():
            print(serilizer.data)
    #     # print(student.is_deleted)E
            print(user)
            return Response({"ok":serilizer.data},status.HTTP_200_OK)

            #     return Response({"serilizer.data":serilizer.data},status.HTTP_200_OK)
            # else:
            #     return Response({"serilizer.data":serilizer.errors},status.HTTP_200_OK)
        else:
            return Response({"ERROR":"LOGIN FIRST"},status.HTTP_400_BAD_REQUEST)
            
                

        # print("This is the student data",student)

        # data = request.user.user_type
        # teacher = Teacher.objects.filter(user_id=user_id, is_deleted=False).last()
        # # print("This is the student fettched",student.last().is_deleted)
        # if teacher is not None:
        #     serilizer = Teacher_Serilizer(teacher)
        #     print(serilizer.data)
        #     # print(student.is_deleted)
        #     if data == "Teacher":
        #         return Response(serilizer.data,status.HTTP_200_OK)
        #     else:
        #         message= {"Message":"You are not Teacher"}
        #         return Response(message,status.HTTP_400_BAD_REQUEST)
        # else:
        #     message= {"Message":f"There is no data, please put some Data first {request.user.first_name}"}
        #     return Response(message,status.HTTP_400_BAD_REQUEST)

        # user_type = User.objects.filter()


#user Login
# class UserLoginView(APIView):
#     def post(self, request):
#         print(request.data)
#         user = authenticate(username=request.data['username'], password=request.data['password'])
#         print("this is the user",user)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=401)


























# class ItemList(generics.ListCreateAPIView):
#     serializer_class = ItemSerializer

#     def get_queryset(self):
#         queryset = Item.objects.all()
#         # type()
#         location = self.request.query_params.get('location')
#         if location is not None:
#             queryset = queryset.filter(itemLocation = location)
#         return queryset


# class ItemSerializerview(APIView):
#     # serializer_class = ItemSerializer



#     pass
    # def get(self,request):
    #     # try:
    #     queryset = Item.objects.all()
    #     # print(queryset)
    #     serializer = ItemSerializer(instance=queryset, many=True)
    #     bike = serializer.data


    #     res = {"Data":serializer.data,"Message":"Data Found Sucessfully"}
    #     return Response(res,status.HTTP_302_FOUND)
    #     # except:
    #         # data = {"Data":"Not Found","Message":"Error Data not fouund"}
    #         # return Response(data, status.HTTP_404_NOT_FOUND)
    
    # def post(self,request):
    #     # try:
    #     data = (request.data)
    #     print(data)
    #     # print(queryset.is_vaild())
        
    #     r = validate_if_id_exist(Location,data['itemLocation'])
    #     if r:
    #         serializer1 = ItemSerializer(data=data)
    #         id_from_request = data['itemLocation']
    #         print("this is the id_from_request", id_from_request)
    #         data_from_location = Location.objects.filter(id=id_from_request).values()
    #         # print("THis is the data_from_location",data_from_location )
    #         # print("I am Here")
    #         if serializer1.is_valid():
    #             # print("hereee")
    #             # print("The serilizer data is ",serializer.data)
    #             serializer1.save()
    #             res = {"Data":serializer1.data,"Location": data_from_location,"Message":"Data saved Sucessfully"}
    #             return Response(res,status.HTTP_202_ACCEPTED)
    #         else:
    #             return Response(serializer1.errors,status.HTTP_202_ACCEPTED)

    #     # except:
    #     else:
    #         # error = "THe location Id doesnt Exist"
    #         data = {"Data":"Location Id Not Found in parent table","Message":"Error Data not fouund"}
    #         return Response(data, status.HTTP_404_NOT_FOUND)