from django.urls import path
from . import views

urlpatterns = [
    path('/<str:username>',views.blog_topic_view.as_view()),
]
