from django.urls import path
from .views import SignUpView, LoginView


urlpatterns = [
    
    path('signup/', SignUpView.as_view(), name= 'signup'),
    path('signup/<str:ref_code>/', SignUpView.as_view(), name = 'signup'),
    path('login/', LoginView.as_view(), name= 'login'),
    ]