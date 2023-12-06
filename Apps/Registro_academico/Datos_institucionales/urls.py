from django.urls import path
from . import views

urlpatterns = [
    path('viewsCourse/', views.ViewsCourse, name='viewsCourse'),
    path('createCourse/', views.CreateCourse, name='createCourse'),
    path('OneViewCourse/<int:id_course>/', views.OneViewCourse, name='oneViewCourse'),
    path('allParticipantsCourse/', views.AllCourseParticipants, name='allParticipantsCourse')
]
