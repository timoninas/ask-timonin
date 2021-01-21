from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from app.views import CreateUserAPIView

urlpatterns = [
    path(r'^create/$', CreateUserAPIView.as_view()),
]