from django.contrib import admin
from .models import Course,Lesson,Attendance,User
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
# admin.site.register(Student)
admin.site.register(Attendance)
# admin.site.register(Roll_Up)