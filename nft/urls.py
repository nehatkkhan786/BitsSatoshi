from django.urls import path
from .views import NftView

urlpatterns = [
    path('', NftView.as_view(), name='bitsNft')
]