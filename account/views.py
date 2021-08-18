from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully register!', 201)



class ActivationView(APIView):
    def get(self, request, email, activation_code):
        # email = request.data.get('email')
        # print(request.data)
        # activation_code = request.data.get('activation_code')
        user = CustomUser.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('This user does not exist', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('MOLODEC!!!', 200)