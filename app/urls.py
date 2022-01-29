from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'location', LocationViewSet)
router.register(r'profilesignup', ProfileSignUpViewSet)
router.register(r'question', MeetingQuestionViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('', login),
    path('index/', index),
    path('uindex/', uindex),
    path('logout/', logout),
    path('location/', add_new_location),
    path('location_list/', location_list_with_user),
    path('csv/', add_new_csv),
    path('user_exist_check/', user_exististan_check),
    path('signup/', signup),
    path('user_onclick/', ListUsersOnClick.as_view()),
    path('check/', UserCheckViewSet.as_view()),
    path('new_meeting/', new_meeting),
    path('meeting_list/', meeting_list),
    path('meetingend/<str:id>', meeting_terminate),
    path('getfile/', getfile),
    path('dlist/', delegate_meeting_list),
    path('home/', user_home),
    path('meetingattend/<str:id>',meetingattend),
    path('answer/<str:id>', answer),
    path('delegtae_answer/<str:id>', delegate_answer),
    path('answer2/', answersubmit),
    path('delegateanswer2/', delegate_answersubmit),
    path('notify/', notification),
    path('ProfileRegistration/', ProfileRegistrationViewSet.as_view()),
    path('logs/<str:id>', logs),
    path('daligate/<str:id>', deligate),
    path('upcomming/', upcomming),
    path('update_user/<int:id>', update_user),
]
