from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AirdropUsers
from django.contrib import messages

# Create your views here.
class AirdropFomrView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'airdrop/airdrop_submit_form.html')

    def post(self, request, *args, **kwargs):
        email = request.user.email
        twitter_username = request.POST.get('twitter_username')
        telegram_username = request.POST.get('telegram_username')
        discord_username = request.POST.get('discord_username')
        tweet_link = request.POST.get('tweet_link')
        trx_address  = request.POST.get('trx_address')

        AirdropUsers.objects.create(email=email, twitter_username = twitter_username, telegram_username=telegram_username, discord_username = discord_username, tweet_link=tweet_link, trx_address=trx_address)
        messages.success(request, 'Thank You! Your form has been submited. Keep referring BitsSatoshi.')
        return redirect('airdrop')

