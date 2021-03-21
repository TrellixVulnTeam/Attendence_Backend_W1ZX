from rest_framework import serializers
from .models import Course,Lesson,Attendance,User



class attendSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields=['id','code_student','url_image','report','check_inf','note']
class info_lesson(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields=['code_student','date','note']
class lessonSerializer(serializers.ModelSerializer):
    # attend=attendSerializer(read_only=True,many=True)
    class Meta:
        model= Lesson
        fields=['name','date']



class courseSerializer(serializers.ModelSerializer):
    # attend = attendSerializer(read_only=True, many=True)
    lessons=lessonSerializer(read_only=True,many=True)
    # student=studentSerializer(read_only=True,many=True)

    # source_name = serializers.CharField(source='source.domain_name')
    class Meta:
        model = Course
        fields=['id',
                'name',
                'code',
                'size',
                'code_major',
                'lecturer',
                'start',
                'end',
                'lessons',
                ]


class userAccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user_name', 'password']
# return information account
class userSerializer(serializers.ModelSerializer):
    # courses=courseSerializer(read_only=True,many=True)
    class Meta:
        model = User
        fields = ['code_user', 'name', 'email', 'major', 'user_type','url_avatar']
# request get information account
class request_get_information_account(serializers.Serializer):
    usercode = serializers.CharField(max_length=100)

class join_course(serializers.Serializer):
    code_course=serializers.CharField(max_length=100)
    code_user=serializers.CharField(max_length=100)
    key_course=serializers.CharField(max_length=100)

class request_attend(serializers.Serializer):
    code_student = serializers.CharField(max_length=20)
    code_course = serializers.CharField(max_length=200)
    date_attend = serializers.DateField()

# request register account
class info_new_account(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    code_user = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=100)
    major = serializers.CharField(max_length=100)
    user_type = serializers.CharField(max_length=10)
#request login
class request_login(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
#create lesson
class request_create_lesson(serializers.Serializer):
    code_course = serializers.CharField(max_length=100)
    code_user = serializers.CharField(max_length=100)
    date_lesson=serializers.DateField()
    name_lesson=serializers.CharField(max_length=100)

#create request create new course
class request_new_course(serializers.Serializer):
    code_user=serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=200)
    size = serializers.IntegerField()
    code_major = serializers.CharField(max_length=20)
    lecturer = serializers.CharField(max_length=100)
    start = serializers.DateField()
    end = serializers.DateField()
    key_course = serializers.CharField(max_length=100)

class request_put_attend(serializers.Serializer):
    code_student=serializers.CharField(max_length=100)

#request info of a lesson
class request_getinfo_alesson(serializers.Serializer):
    code_course = serializers.CharField(max_length=200)
    date_attend = serializers.DateField()

#request info of a course
class request_getinfo_acourse(serializers.Serializer):
    code_course=serializers.CharField(max_length=200)
#request report of attendent
class request_report_attend(serializers.Serializer):
    note=serializers.CharField(max_length=100000)
#request post avatar for user
class request_post_avatar(serializers.Serializer):
    usercode=serializers.CharField(max_length=100)
    image=serializers.CharField(min_length=0)

# request change information of attendance(lecturer do)
class request_change_information_roll_up(serializers.Serializer):
    code_student=serializers.CharField(max_length=100,allow_null=True,allow_blank=True)
    report = serializers.BooleanField()
    check_inf = serializers.BooleanField()
    note = serializers.CharField(max_length=1000000,allow_null=True,allow_blank=True)