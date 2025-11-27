from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from .models import User
from .serializers import RegisterSerializer

# Inscription
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

# Login JWT
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
