from django.db import models


class Student(models.Model):
    registration_no = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    branch = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    email_id = models.EmailField()
    campus = models.CharField(max_length=20)

    def __str__(self):
        return self.registration_no


class Course(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    basket = models.IntegerField()
    branch = models.CharField(max_length=10)
    credits = models.IntegerField()

    def __str__(self):
        return self.code + '-' + self.name


class Grade(models.Model):
    student_id = models.ForeignKey(Student)
    course_id = models.ForeignKey(Course)
    grade_secured = models.CharField(max_length=1)
    unique_id = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.student_id.registration_no + '-' + self.course_id.code + '-' + self.grade_secured


class CGPA(models.Model):
    student_id = models.OneToOneField(Student)
    total_points = models.IntegerField()
    total_credits = models.IntegerField()
    back_papers = models.IntegerField()
    cgpa_secured = models.FloatField()

    def __str__(self):
        return self.student_id.registration_no + '-' + str(self.cgpa_secured)