from django.urls import path
from login import views as login_views

urlpatterns = [
  path("", login_views.index,name="index"),
  path("login/", login_views.login),
  path("register/", login_views.register),
  path("logout/", login_views.logout),
  path("attendance/", login_views.attendance_view),
]
