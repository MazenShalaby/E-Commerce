from django.urls import path

from .views import register

# create your urlpatterns here.

urlpatterns = [
    path("register/", register, name='register')
]
