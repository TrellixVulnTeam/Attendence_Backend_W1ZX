import base64
import os
from os import curdir, sep
from PIL import Image
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializer import courseSerializer, attendSerializer, lessonSerializer, request_attend, join_course, \
    info_new_account, request_login, userSerializer, request_create_lesson, \
    request_new_course, request_put_attend, request_getinfo_alesson, info_lesson, request_getinfo_acourse, \
    request_report_attend, request_get_information_account, request_change_information_roll_up, request_post_avatar

from .models import Course, Lesson, Attendance, User


# Create your views here.
class get_courses(APIView):
    def get(self, request):
        list_Course = Course.objects.all()
        mData = courseSerializer(list_Course, many=True)
        return Response(mData.data, status=status.HTTP_200_OK)


# get information account
class get_inf_account(APIView):
    def post(self, request):
        mdata = request_get_information_account(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)
        userCode = mdata.data['usercode']
        user = User.objects.filter(code_user=userCode).first()
        response = userSerializer(user)
        return Response(response.data, status=status.HTTP_200_OK)


# create new account
class register(APIView):
    def post(self, request):
        # notification for client
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }
        response_False = {
            "ok": False,
            "massage": "Tài khoản đã tồn tại"
        }
        mdata = info_new_account(data=request.data)
        # Check asking for data
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)
        # gán dữ liêu
        user_name = mdata.data['user_name']
        password = mdata.data['password']
        code_user = mdata.data['code_user']
        name = mdata.data['name']
        email = mdata.data['email']
        major = mdata.data['major']
        user_type = mdata.data['user_type']
        # tài khoản đã tồn tại chưa
        user = User.objects.filter(user_name=user_name).first()
        if (user != None):
            return Response(response_False, status=status.HTTP_200_OK)
        # create new account
        User.objects.create(user_name=user_name, password=password, code_user=code_user, name=name, email=email,
                            major=major, user_type=user_type)
        return Response(response_True, status=status.HTTP_200_OK)


# login
class login(APIView):
    def post(self, request):
        # notification for client

        response_False = {
            "ok": False,
            "massage": "sai tên tài khoản hoặc mật khẩu"
        }
        mdata = request_login(data=request.data)
        if not mdata.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_name = mdata.data['user_name']
        password = mdata.data['password']
        user = User.objects.filter(user_name=user_name, password=password).first()
        if (user == None):
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        response = courseSerializer(user.courses.all(), many=True)
        response_True = {
            "code_user": user.code_user,
            "user_type": user.user_type,
            "courses": response.data
        }
        return Response(response_True, status=status.HTTP_200_OK)


# log out

# get url image student rolled Up
class image(APIView):
    def post(self, request):
        mdata = request_attend(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)
        code_student = mdata.data['code_student']
        code_course = mdata.data['code_course']
        date_attend = mdata.data['date_attend']

        listattend = Attendance.objects.filter(code_course=code_course, date=date_attend)
        if (listattend == None):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (listattend.filter(code_student=code_student).first() != None):
            attend = listattend.filter(code_student=code_student)
            response = attendSerializer(attend, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        response = attendSerializer(listattend, many=True)
        return Response(response.data, status=status.HTTP_200_OK)


# thay doi thông tin cho diem danh
class AttendentDetail(APIView):

    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }
        response_False = {
            "ok": False,
            "massage": "Bạn đã thay đổi thông tin trước đó"
        }
        attend = self.get_object(pk)
        mdata = request_put_attend(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)
        if (attend.check_inf == False):
            attend.code_student = mdata.data['code_student']
            attend.check_inf = True
            attend.save()
            return Response(response_True, status=status.HTTP_200_OK)
        return Response(response_False, status=status.HTTP_200_OK)


# report hình ảnh khi có người thay đổi thông tin trước đó rồi
class AttendentReport(APIView):

    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }

        attend = self.get_object(pk)
        mdata = request_report_attend(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)

        attend.note = mdata.data['note']
        attend.report = True
        attend.save()
        return Response(response_True, status=status.HTTP_200_OK)


# lecturer set information for roll up of student
class Set_Info_RollUp(APIView):
    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }

        attend = self.get_object(pk)
        mdata = request_change_information_roll_up(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu rooi", status=status.HTTP_404_NOT_FOUND)
        attend.code_student = mdata.data['code_student']
        attend.note = mdata.data['note']
        attend.report = mdata.data['report']
        attend.check_inf = mdata.data['check_inf']
        attend.save()
        return Response(response_True, status=status.HTTP_200_OK)


# create lesson for course
class create_lesson(APIView):
    def post(self, request):
        mdata = request_create_lesson(data=request.data)
        if not mdata.is_valid():
            return Response('ầ', status=status.HTTP_400_BAD_REQUEST)
        code_user = mdata.data['code_user']
        code_course = mdata.data['code_course']
        date_lesson = mdata.data['date_lesson']
        name_lesson = mdata.data['name_lesson']
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }
        response_False = {
            "ok": False,
            "massage": "Thất bại"
        }
        user = User.objects.filter(code_user=code_user).first()
        if (user.user_type == 'lecturer'):
            print(user.user_type)
            course = Course.objects.filter(code=code_course).first()
            date = course.lessons.filter(date=date_lesson).first()
            if (date == None):
                course.lessons.create(name=name_lesson, date=date_lesson)
                return Response(response_True, status=status.HTTP_200_OK)
        else:
            return Response(response_False, status=status.HTTP_200_OK)
        return Response(response_False, status=status.HTTP_404_NOT_FOUND)


# create a new course
class create_new_course(APIView):
    def post(self, request):
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }
        response_False = {
            "ok": False,
            "massage": "Thất bại"
        }
        mdata = request_new_course(data=request.data)
        if not mdata.is_valid():
            return Response(response_False, status=status.HTTP_404_NOT_FOUND)
        code_user = mdata.data['code_user']
        code = mdata.data['code']
        name = mdata.data['name']
        size = mdata.data['size']
        code_major = mdata.data['code_major']
        lecturer = mdata.data['lecturer']
        start = mdata.data['start']
        end = mdata.data['end']
        key_course = mdata.data['key_course']

        user = User.objects.filter(code_user=code_user).first()
        if (user.user_type != 'student'):
            course = user.courses.filter(code=code).first()
            if (course != None):
                return Response(response_False, status=status.HTTP_404_NOT_FOUND)
            user.courses.create(code=code
                                , name=name
                                , size=size
                                , code_major=code_major
                                , lecturer=lecturer
                                , start=start
                                , end=end
                                , key_course=key_course)
            return Response(response_True, status=status.HTTP_200_OK)
        return Response(response_False, status=status.HTTP_404_NOT_FOUND)


class join(APIView):
    def post(self, request):
        mdata = join_course(data=request.data)
        if not mdata.is_valid():
            return Response(status=status.HTTP_404_NOT_FOUND)
        code_user = mdata.data['code_user']
        code_course = mdata.data['code_course']
        key_course = mdata.data['key_course']
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }
        response_False = {
            "ok": False,
            "massage": "Thất bại"
        }
        # kiểm tra coi lớp nào có mã lớp và key là như vậy
        course = Course.objects.filter(code=code_course, key_course=key_course).first()
        if (course == None):
            return Response(response_False, status.HTTP_404_NOT_FOUND)
        # tìm user có mã user là ...
        user = User.objects.filter(code_user=code_user).first()
        user.courses.add(course)
        return Response(response_True, status=status.HTTP_200_OK)


# get info lesson
class infolesson(APIView):
    def post(self, request):
        mdata = request_getinfo_alesson(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)

        code_course = mdata.data['code_course']
        date_attend = mdata.data['date_attend']
        response_False = {
            "ok": False,
            "massage": "Thất bại"
        }
        listattend = Attendance.objects.filter(code_course=code_course, date=date_attend)
        if (listattend == None):
            return Response(status=status.HTTP_404_NOT_FOUND)

        response = info_lesson(listattend, many=True)
        return Response(response.data, status=status.HTTP_200_OK)


# get info a course
class infocourse(APIView):
    def post(self, request):
        mdata = request_getinfo_acourse(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)
        code_course = mdata.data['code_course']

        listattend = Attendance.objects.filter(code_course=code_course)
        if (listattend == None):
            return Response(status=status.HTTP_404_NOT_FOUND)

        x = sorted(listattend, key=lambda Attendent: Attendent.date)
        response = info_lesson(x, many=True)

        return Response(response.data, status=status.HTTP_200_OK)


# give image from client and save to server
class change_avatar_account(APIView):
    def post(self, request):
        mdata=request_post_avatar(data=request.data)
        if not mdata.is_valid():
            return Response("sai dữ liêu", status=status.HTTP_404_NOT_FOUND)
        response_True = {
            "ok": True,
            "massage": "Thành công"
        }
        usercode=mdata.data['usercode']
        image=mdata.data['image']
        user=User.objects.filter(code_user=usercode).first()
        # decode Base64 from string to image
        img = base64.b64decode(image)
        # ulr to save image
        path="media/avatar/"
        filename = path+str(usercode)+".jpg";
        # save image to url
        with open(filename, 'wb') as f:
            f.write(img)
        f.close()
        user.url_avatar="/"+filename
        user.save()


        return Response(response_True,status=status.HTTP_200_OK)

# class UserList(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = Get_Courses
#
#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = Get_Courses(queryset, many=True)
#         return Response(serializer.data)

# class url_student(APIView):
#
#     def get_object(self):
#         try:
#             return Course.objects.all()
#         except Course.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object()
#
#         serializer = lessonSerializer(snippet)
#         return Response(serializer.data)
