from django.shortcuts import render
from django.views import View

# Create your views here.
class AirdropFomrView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'airdrop/airdrop_submit_form.html')