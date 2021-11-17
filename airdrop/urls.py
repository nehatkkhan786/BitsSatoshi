from django.urls import path
from .views import AirdropFomrView


urlpatterns = [
    path('', AirdropFomrView.as_view(), name ='airdrop'),
]