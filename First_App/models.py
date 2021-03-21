
from django.db import models
# from django.contrib.auth.models import
#import to can use ArrayField
from django.utils.timezone import now
import datetime
# Create your models here.
class Attendance(models.Model):
    code_course=models.CharField(max_length=100)
    code_student=models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField(auto_now_add=False)
    url_image = models.CharField(max_length=1000,null=True)
    report=models.BooleanField(default=False)
    check_inf=models.BooleanField(default=False)
    note=models.TextField(null=True,blank=True)

class Lesson(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(blank=True,null=True)
    def __str__(self):
        return '%s %s' % (self.name, self.date)

class Course(models.Model):
    code = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=200)
    size = models.IntegerField()
    code_major= models.CharField(max_length=20)
    lecturer = models.CharField(max_length=100)
    start = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False,auto_now_add=False)
    key_course=models.CharField(max_length=100,null=True,blank=True)
    lessons =models.ManyToManyField(Lesson)
    # student = models.ManyToManyField(Student)
# class Roll_Up(models.Model):
#     Course=models.ForeignKey('Course',related_name='Courses',on_delete=models.CASCADE)
#     Item_Roll_Up=models.ForeignKey(Item_Roll_Up,related_nameItem_Roll_Up',on_delete=models.CASCADE)

class User(models.Model):
    user_name=models.CharField(max_length=100,null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    code_user=models.CharField(max_length=100)
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=100)
    major=models.CharField(max_length=100)
    user_type=models.CharField(max_length=10)
    courses=models.ManyToManyField(Course,blank=True)
    url_avatar=models.CharField(max_length=100,null=True,blank=True)







