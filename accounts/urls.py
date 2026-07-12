from django.urls import path

from .views import register, login_view, activate_registered_account

# create your urlpatterns here.

urlpatterns = [
    path("register/", register, name='register'),
    path("login/", login_view, name='login'),
    path("activate/<user_id_64>/<token>/", activate_registered_account, name='activate'),
]
