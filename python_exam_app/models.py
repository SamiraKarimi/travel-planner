from django.db import models
import re, bcrypt
from datetime import date

class UserManager(models.Manager):
    def registerationValidator(self,postData):
        validationErrors = {}
        if len(postData['fname'])<3:
            validationErrors['fname']= "the Name must be at least three character"
        if len(postData['uname'])<3:
            validationErrors['uname']='the Username must be at least three character'
        if len(User.objects.filter(user_name= postData['uname']))>0:
            validationErrors['reserved']="this Username already reserved"
        if len(postData['pw'])<8:
            validationErrors['pw']='password must be eight character'
        if postData['pw'] != postData['cpw']:
            validationErrors['pw']='please enter a valid password'
        if len(User.objects.filter(user_name = postData['uname']))>0:
            validationErrors['reserved']="this Username already reserved"
        return validationErrors
    def loginValidator(self,postData1):
        loginErrors = {}
        result=User.objects.filter(user_name=postData1['uname'])
        if len(result)==0:
            loginErrors['notExist']='Username not found'
        else:
            user = result[0]
            if not bcrypt.checkpw(postData1['pw'].encode(), user.password.encode()):
                loginErrors['pw']='Password does not match'
        return loginErrors
class tripManager(models.Manager):
    def validateItem(self,forminfo):
        errors = {}
        # validaton code here
        print(forminfo)
        if len(forminfo['dest'])<1:
            errors['destRequired']='detination is  required!'
        if len(forminfo['descrip'])<1:
            errors['descRequired']='description is  required!'
        if len(forminfo['dateFrom'])<1:
            errors['datefromRequired']='date from is required!'
        if len(forminfo['dateTo'])<1:
            errors['datetoRequired']='date to required!'
        print(f'^&&&&&&&&&&&&&'*5)
        today = str(date.today())
        print(today) 
        print(forminfo['dateFrom'])
        if forminfo['dateFrom']<today:
            errors['dateFromInvalid']='date should be in future'
        if forminfo['dateFrom']>forminfo['dateTo']:
            errors['dateInvalid']='date is not valid'
        print(errors)
        return errors


class User(models.Model):
    name= models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()


class Trip(models.Model):
    destination= models.CharField(max_length=255)
    description= models.CharField(max_length=255,null=False)
    uploader = models.ForeignKey(User, related_name = 'trips_uploaded', on_delete = models.CASCADE)
    planner = models.ManyToManyField(User, related_name ='plan_trips')
    DateTo=models.DateField(blank=False, null=False)
    DateFrom=models.DateField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = tripManager()