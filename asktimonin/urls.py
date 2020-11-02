"""asktimonin URL Configuration
 `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions),
    path('new_questions', views.new_questions, name='newquestions'),
    path('ask_question', views.ask_question, name='askquestion'),
    path('answer_question', views.answer_question, name='answerquestion'),
    path('tag', views.tag_questions, name='tagquestions'),
    path('settings', views.settings, name='settings'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('question/<int:pk>/', views.question_page),
    path('tag/<str:pk>/', views.tag_page),
]
