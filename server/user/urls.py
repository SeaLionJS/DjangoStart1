from django.urls import path, include

from . import views

urlpatterns = [
    path('profile-info/', views.UserView.as_view()),
    #....
    path('update-user/', views.UserUpdateAPIView.as_view(), name="update-user"),
]
