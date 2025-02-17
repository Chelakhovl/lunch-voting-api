from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    LogoutSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API for user registration.
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login to include user details in response.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle login request and return user details with JWT tokens.
        """
        response = super().post(request, *args, **kwargs)
        user = User.objects.filter(email=request.data.get("email")).first()

        if user:
            response.data["user"] = UserSerializer(user).data

        return response


class LogoutView(generics.GenericAPIView):
    """
    API for user logout (blacklist refresh token).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        """
        Handle logout request, blacklisting the refresh token.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    API for retrieving authenticated user profile.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
