from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, status, generics

# Create your views here.
from django.shortcuts import render
from .models import User, UserProfile

# структура json
# {
#     "first_name": "Богдан",
#     "middle_name": "Богданов",
#     "last_name": "Богданович",
#     "email": "b@mail.com",
#     "id": "ffb875-5323-418b-9a9a-1234567",
#     "photo": "/media/images/ffa9b875-5323-418b-9a9a-7f6fe44cabc8/logo/logo.jpeg",
#     "phone": "0990000000",
#     "date_joined": "2000-06-13T10:50:44+03:00",
#     "creation_rules": true,
#     "comment_rules": true,
#     "profile_view_rules": true,
#     "show_email": false,
#     "show_phone": false,
#     "userprofile": {
#         'birth_date' : "2000-06-13T10:50:44+03:00", 
#         'status': "життя прекрасне!", 
#         'description': "текстовий опис", 
#         'show_birth_date': false
#     }
# }

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()


    def update(self, request, *args, **kwargs):
        # портібний код
        # оновлюємо користувача по id з вхідних даних
        return Response({"detail": "success", "data": "відформатовані дані про користувача"})

  
    
class UserView(APIView):
    def get(self, request):
        # отримання даних користувача
        # насправді є аутентифікація і є request.user
        # але у даній роботі хай email користувача передається через query params get-запита
        # потрібно по email знайти користувача і відправити на клієнт (але без пароля, відповідно до структури вище)

        return Response({"detail": "success", 'data': "дані про користувача"}, status=status.HTTP_200_OK)

