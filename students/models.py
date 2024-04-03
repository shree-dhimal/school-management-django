from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser, BaseUserManager

# Create your models here.

# class UserManager(BaseUserManager):
#     # user_name = models.CharField(max_length = 50, unique = True)
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True')
        
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True')
        
#         return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    user_type = ( 
    ("Student", "Student"), 
    ("Teacher", "Teacher"),
    ("Management", "Management")) 
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(choices = user_type, max_length=50, default = 'Teacher')
    
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    # name = models.CharField(max_length=255, unique=False)
    roll = models.IntegerField()
    date_of_birth = models.DateField()
    is_deleted = models.BooleanField(default = False)


class Subjects(models.Model):
    Faculty = ( 
    ("Science", "Science"), 
    ("Management", "Management"),
    ("IT", "IT"),) 
    name = models.CharField(max_length=30)
    faculty = models.CharField(choices = Faculty, max_length=50, default = 'IT')
    is_deleted = models.BooleanField(default = False)

class Teacher(models.Model):
    name = models.ForeignKey(User, on_delete= models.CASCADE)
    date_of_birth = models.DateField()
    subject_name = models.ForeignKey(Subjects, on_delete= models.CASCADE)
    is_deleted = models.BooleanField(default = False)


    











# class Location(models.Model):
#     locationName = models.CharField(max_length=100,unique=False)
#     locationCountry = models.CharField(max_length=100, default="Nepal")
#     Country_code = models.IntegerField(default= 0)
#     zip_code = models.CharField(max_length=100)

#     def __str__(self):
#         return self.locationName
    
# class Item(models.Model):
#     itemName = models.CharField(max_length = 100)
#     dateAdded = models.DateField(auto_now_add= True)
#     itemLocation = models.ForeignKey(Location, on_delete= models.CASCADE)
#     # itemCountry = models.ForeignKey(Locaion, on_delete= models.CASCADE)
#     # def __str__(self):
#     #     return self.itemName

# class Bike(models.Model):
#     name = models.CharField(max_length = 100)
#     model = models.DateField(max_length = 100)
#     manufacture_date = models.DateField(max_length = 100)
#     brand = models.ForeignKey(Item, on_delete= models.CASCADE)

#     def manufactureyear(self):
#          return self.manufacture_date.strftime('%Y')
       

    