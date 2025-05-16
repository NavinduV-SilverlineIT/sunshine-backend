from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status

class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            role = "SuperAdmin" if user.is_superuser else "Admin"
            refresh = RefreshToken.for_user(user)
            res = Response()
            res.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                samesite='Lax',
                secure=False,
            )
            res.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                samesite='Lax',
                secure=False,
            )
            res.data = {
                "message": "Login successful",
                "username": user.username,
                "email": user.email,
                "role": role,
            }
            return res

        return Response({"error": "Invalid credentials or not admin"}, status=status.HTTP_401_UNAUTHORIZED)

class AdminLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            res = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            res.delete_cookie('access_token')
            res.delete_cookie('refresh_token')
            return res

        except Exception as e:
            return Response({"error": "Logout failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)