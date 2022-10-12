from django.urls import path
from . import views

urlpatterns = [
    path('/sms', views.sendSMS_view),
    path('/emailcode', views.sendmail_view),
    path('/<str:username>/avatar', views.update_avatar_view),
    path('/<str:username>/password', views.update_password_view),
    path('/<str:username>', views.UserView.as_view()),
    path('', views.UserView.as_view()),
]
