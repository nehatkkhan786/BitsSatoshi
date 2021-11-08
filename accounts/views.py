from django.shortcuts import render, redirect
from django.views import View
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages, auth

# Create your views here.

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        code = str(kwargs.get('ref_code'))
        try:
            profile = Profile.objects.get(code=code)
            request.session['ref_profile'] = profile.id
            print('id', profile.id)
        except:
            pass
        print(request.session.get_expiry_date())
        return render(request, 'accounts/signup.html')

    def post(self, request, *args, **kwargs):
        profile_id = request.session.get('ref_profile')
        print('profile_id', profile_id)

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is not available')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already is use')
                else:
                    if profile_id is not None:
                        recommended_by_profile = User.objects.get(id=profile_id)
                        instance = User.objects.create_user(username=username, email=email, password=password1)
                        instance.save()
                        print('usersaved')
                        registered_user = User.objects.get(id=instance.id)
                        registered_profile = Profile.objects.get(user=registered_user)
                        registered_profile.recommended_by = recommended_by_profile.username
                        registered_profile.save()
                        print('user created')
                        return redirect('homepage')
                    else:
                        user = User.objects.create_user(username=username, email=email, password=password1)
                        user.save()
                        print('user created without recommended_by_profile')
                        return redirect('homepage')
            

        else:
            messages.error(request, "Password Didnt Match")
            return redirect('signup')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')


    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are successfully Log in")
            print("You are successfully Log in")
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid Credentials')
            print('invalid Credentials')
            return redirect('login')


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You are successfully Logout")
        return redirect('homepage')
