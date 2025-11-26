# views.py
from rest_framework import generics
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# Create your views here.
from rest_framework.permissions import IsAuthenticated

class MeView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
