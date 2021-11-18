from django.urls import path
from .views import SignUpView, LoginView, EmailVerification, DashboardView, PasswordResetView,PasswordResetEmailView, CreateNewPasswordView, LogoutView, AccountCreatedView, AccountVerifiedView, RecommendedView


urlpatterns = [
    
    path('signup/', SignUpView.as_view(), name= 'signup'),
    path('signup/<str:ref_code>/', SignUpView.as_view(), name = 'signup'),
    path('email_verification/<uidb64>/<token>/', EmailVerification, name = 'email_verification'),
    path('login/', LoginView.as_view(), name= 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dasboard/', DashboardView.as_view(), name='dashboard'),
    path('password_reset/', PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_email/<uidb64>/<token>/', PasswordResetEmailView.as_view(), name='password_reset_email'),
    path('create_new_password/', CreateNewPasswordView.as_view(),name='create_new_password'),


    path('account_created/', AccountCreatedView.as_view(), name ='account_created'),
    path('account_verified/', AccountVerifiedView.as_view(), name ='account_verified'),
    path('recomendations/', RecommendedView.as_view(), name= 'my_recommendations'),
    ]