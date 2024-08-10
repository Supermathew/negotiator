# accounts/views.py

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from accounts.models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer,UserChangePasswordSerializer,UpdateNameSerializer,AccountDetailSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .renderers import UserRenderer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


Account = get_user_model()


class RegisterAPIView(APIView):
    
    renderer_classes = [UserRenderer]
    def post(self, request, *args, **kwargs):
        print("my nae sfbsjfn")
        serializer = RegistrationSerializer(data=request.data)
        # print(serializer)
        print("hello world")
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            profile_data = {
                'user': user.id,
                'phone_number': user.phone_number,
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = serializer.validated_data['email']
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({
                'message': 'Registration successful. An email has been sent to your registered email address. Please verify it.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateNameAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateNameSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = AccountDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    
    renderer_classes = [UserRenderer]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message':"User login successfully",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserProfileAPIView(APIView):
    
    # authentication_classes = [JWTAuthentication]
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        if UserProfile.objects.filter(user=request.user).exists():
            return Response({"message": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
import os




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
    
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)



class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset Successfully'}, status=status.HTTP_200_OK)



class ActivateAccountAPIView(APIView):
    
    renderer_classes = [UserRenderer]
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Congratulations! Your account is activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)
        
        