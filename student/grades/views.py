from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CGPA
from .models import Course
from .models import Grade
from .models import Student
from .serializers import CGPASerializer
from .serializers import CourseSerializer
from .serializers import GradeSerializer
from .serializers import OneCourseManyStudentsSerializer
from .serializers import OneStudManyCoursesSerializer
from .serializers import StudentSerializer


class StudentList(APIView):

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SingleStudent(APIView):

    def get_object(self, pk):
        try:
            return Student.objects.get(registration_no = pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseList(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SingleCourse(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(code = pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GradeList(APIView):

    def cgpa_entry(self, sid, cid, gs):
        cgpa = CGPA.objects.filter(student_id=sid)
        course = Course.objects.filter(code=cid)
        credit = course[0].credits
        student_id = sid
        if cgpa:
            grade_char = gs
            back_papers = cgpa[0].back_papers
            total_points = cgpa[0].total_points
            total_credits = cgpa[0].total_credits
            cgpa_secured = cgpa[0].cgpa_secured
            grade_list = ["O", "E", "A", "B", "C", "D"]
            if grade_char in grade_list:
                grade_point = 10 - grade_list.index(grade_char)
                total_points = total_points + (grade_point*credit)
                total_credits = total_credits + credit
                cgpa_secured = total_points / total_credits
            elif grade_char == "F":
                back_papers += 1
            cgpa_data = {'student_id': student_id, 'total_points': total_points, 'total_credits': total_credits, 'cgpa_secured': cgpa_secured, 'back_papers': back_papers}
            serializer = CGPASerializer(cgpa[0], data=cgpa_data)
            if serializer.is_valid():
                serializer.save()
        else:
            grade_char = gs
            grade_list = ["O", "E", "A", "B", "C", "D"]
            total_credits = 0
            total_points = 0
            back_papers = 0
            cgpa_secured = 0.0
            if grade_char in grade_list:
                cgpa_secured = float(10 - grade_list.index(grade_char))
                total_credits = credit
                total_points = credit * cgpa_secured
            elif grade_char == "F":
                back_papers += 1
            else:
                return False
            cgpa_data = {'student_id': student_id, 'total_points': total_points, 'total_credits': total_credits, 'cgpa_secured': cgpa_secured, 'back_papers': back_papers}
            cgpa_serializer = CGPASerializer(data=cgpa_data)
            if cgpa_serializer.is_valid():
                cgpa_serializer.save()

    def get(self, request):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'student_id' in request.data.keys() and 'course_id' in request.data.keys():
            request.data['unique_id'] = request.data['student_id'] + request.data['course_id']
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            self.cgpa_entry(request.data['student_id'], request.data['course_id'], request.data['grade_secured'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SingleGrade(APIView):

    def cgpa_delete(self, sid, cid, grade):
        cgpa = CGPA.objects.filter(student_id=sid)
        course = Course.objects.filter(code=cid)
        credit = course[0].credits
        student_id = sid
        if cgpa:
            grade_char = grade.grade_secured
            back_papers = cgpa[0].back_papers
            total_points = cgpa[0].total_points
            total_credits = cgpa[0].total_credits
            cgpa_secured = cgpa[0].cgpa_secured
            grade_list = ["O", "E", "A", "B", "C", "D"]
            if grade_char == 'F':
                back_papers -= 1
            else:
                grade_point = 10 - grade_list.index(grade_char)
                total_points = total_points - (grade_point * credit)
                total_credits = total_credits - credit
                cgpa_secured = total_points / total_credits
            cgpa_data = {'student_id': student_id, 'total_points': total_points, 'total_credits': total_credits, 'cgpa_secured': cgpa_secured, 'back_papers': back_papers}
            serializer = CGPASerializer(cgpa[0], data=cgpa_data)
            if serializer.is_valid():
                serializer.save()

    def cgpa_entry(self, sid, cid, gs, grade):
        cgpa = CGPA.objects.filter(student_id=sid)
        course = Course.objects.filter(code=cid)
        credit = course[0].credits
        student_id = sid
        if cgpa:
            grade_char = gs
            back_papers = cgpa[0].back_papers
            total_points = cgpa[0].total_points
            total_credits = cgpa[0].total_credits
            cgpa_secured = cgpa[0].cgpa_secured
            grade_list = ["O", "E", "A", "B", "C", "D"]
            if grade.grade_secured == 'F':
                back_papers -= 1
            else:
                grade_point = 10 - grade_list.index(grade.grade_secured)
                total_points = total_points - (grade_point * credit)
                total_credits = total_credits - credit
                cgpa_secured = total_points / total_credits
            if grade_char in grade_list:
                grade_point = 10 - grade_list.index(grade_char)
                total_points = total_points + (grade_point*credit)
                total_credits = total_credits + credit
                cgpa_secured = total_points / total_credits
            elif grade_char == "F":
                back_papers += 1
            cgpa_data = {'student_id': student_id, 'total_points': total_points, 'total_credits': total_credits, 'cgpa_secured': cgpa_secured, 'back_papers': back_papers}
            serializer = CGPASerializer(cgpa[0], data=cgpa_data)
            if serializer.is_valid():
                serializer.save()
        else:
            grade_char = gs
            grade_list = ["O", "E", "A", "B", "C", "D"]
            total_credits = 0
            total_points = 0
            back_papers = 0
            cgpa_secured = 0.0
            if grade_char in grade_list:
                cgpa_secured = float(10 - grade_list.index(grade_char))
                total_credits = credit
                total_points = credit * cgpa_secured
            elif grade_char == "F":
                back_papers += 1
            else:
                return False
            cgpa_data = {'student_id': student_id, 'total_points': total_points, 'total_credits': total_credits, 'cgpa_secured': cgpa_secured, 'back_papers': back_papers}
            cgpa_serializer = CGPASerializer(data=cgpa_data)
            if cgpa_serializer.is_valid():
                cgpa_serializer.save()

    def get_object(self, sid, cid):
        try:
            return Grade.objects.get(unique_id = sid+cid)
        except Grade.DoesNotExist:
            raise Http404

    def get(self, request, sid, cid):
        grade = self.get_object(sid, cid)
        serializer = GradeSerializer(grade, many=False)
        return Response(serializer.data)

    def put(self, request, sid, cid):
        grade = self.get_object(sid, cid)
        request.data['unique_id'] = request.data['student_id']+request.data['course_id']
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            self.cgpa_entry(request.data['student_id'], request.data['course_id'], request.data['grade_secured'], grade)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sid, cid):
        grade = self.get_object(sid, cid)
        self.cgpa_delete(sid, cid, grade)
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OneStudentManyCourses(APIView):

    def get(self, request, sid):
        grade = Grade.objects.filter(student_id=sid)
        serializer = OneStudManyCoursesSerializer(grade, many=True)
        return Response({sid: serializer.data})


class OneCourseManyStudents(APIView):

    def get(self, request, cid):
        grade = Grade.objects.filter(course_id=cid)
        serializer = OneCourseManyStudentsSerializer(grade, many=True)
        return Response({cid: serializer.data})


class CGPAList(APIView):

    def get(self, request):
        grades = CGPA.objects.all()
        serializer = CGPASerializer(grades, many=True)
        return Response(serializer.data)

