# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.api.views import RegisterAPIView, LoginAPIView, LogoutView, UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,ActivateAccountAPIView,UserProfileAPIView,UpdateNameAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('personal-details/', UpdateNameAPIView.as_view(), name='update-name'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('activate/<uidb64>/<token>/', ActivateAccountAPIView.as_view(), name='activate'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),

]

