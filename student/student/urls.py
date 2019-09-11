"""student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from grades import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^student/', views.StudentList.as_view()),
    url(r'^course/', views.CourseList.as_view()),
    url(r'^grade/', views.GradeList.as_view()),
    url(r'^cgpa/', views.CGPAList.as_view()),
    url(r'^singlestudent/(?P<pk>\w+)/', views.SingleStudent.as_view()),
    url(r'^singlecourse/(?P<pk>\w+)/', views.SingleCourse.as_view()),
    url(r'^singlegrade/(?P<sid>\w+)/(?P<cid>\w+)/', views.SingleGrade.as_view()),
    url(r'^onestudmanygrades/(?P<sid>\w+)/', views.OneStudentManyCourses.as_view()),
    url(r'^onecoursemanygrades/(?P<cid>\w+)/', views.OneCourseManyStudents.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
