from rest_framework import serializers
from .models import Student
from .models import Course
from .models import Grade
from .models import CGPA


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'


class OneCourseManyStudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('student_id', 'grade_secured')


class OneStudManyCoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('course_id', 'grade_secured')


class CGPASerializer(serializers.ModelSerializer):

    class Meta:
        model = CGPA
        fields = '__all__'

