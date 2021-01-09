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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions, name='newquestions'),
    path('new_questions/', views.new_questions, name='newquestions'),
    path('hot_questions/', views.hot_questions, name='hotquestions'),
    path('ask_question/', views.ask_question, name='askquestion'),
    path('tag/', views.tag_questions, name='tagquestions'),
    path('settings/', views.settings, name='settings'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('question/<int:pk>/', views.question_page, name='selectedquestion'),
    path('tag/<str:pk>/', views.tag_page, name='tagquestions'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()