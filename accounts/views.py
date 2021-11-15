from django.shortcuts import render, redirect
from django.views import View
from accounts.models import Profile
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib import messages, auth
from django.contrib.auth import logout


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.contrib.auth.mixins import LoginRequiredMixin


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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = email.split('@')[0]


        if password1==password2:
            if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email already is use')
            else:
                if profile_id is not None:
                    recommended_by_profile = CustomUser.objects.get(id=profile_id)
                    instance = CustomUser.objects.create_user(first_name =first_name, last_name=last_name, email=email, password=password1, username=username)
                    instance.save()
                    print('usersaved')
                    registered_user = CustomUser.objects.get(id=instance.id)
                    registered_profile = Profile.objects.get(user=registered_user)
                    registered_profile.recommended_by = recommended_by_profile
                    registered_profile.save()

                    current_site = get_current_site(request)
                    mail_subject = "Account Activation"
                    message = render_to_string("accounts/email_verification.html", {
                        'user': instance, 
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                        'token': default_token_generator.make_token(instance)
                    })
                    send_mail = EmailMessage(mail_subject, message, to=[email])
                    print(send_mail)
                    send_mail.send()
                    messages.success(request, "Account Created! We have sent you an email to verify your Account.")
                    print('user created')
                    return redirect('account_created')

                else:
                    user = CustomUser.objects.create_user(first_name = first_name, last_name=last_name, email=email, password=password1, username=username)
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = "Account Activation"
                    message = render_to_string("accounts/email_verification.html", {
                        'user': user, 
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    send_mail = EmailMessage(mail_subject, message, to=[email])
                    print(send_mail)
                    send_mail.send()
                    print('user created without recommended_by_profile')
                    return redirect('account_created')
        else:
            messages.error(request, "Password Didnt Match")
            return redirect('signup')




def EmailVerification(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = CustomUser.objects.get(pk=uid)

	except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Thank You! Your account is successfully activated.')
		return redirect('account_verified')
	else:
		messages.error(request, 'Sorry something went wrong!')
		return redirect('signup')



class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')


    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are successfully Log in")
            print("You are successfully Log in")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            print('invalid Credentials')
            return redirect('login')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You are successfully Logout")
        return redirect('homepage')



class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/dashboard.html')



class PasswordResetView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'accounts/password_reset.html')

	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		if CustomUser.objects.filter(email__iexact=email).exists():
			user = CustomUser.objects.get(email=email)
			current_site = get_current_site(request)
			mail_subject = 'Password Reset'
			message = render_to_string('accounts/password_reset_email.html', {

					'user':user,
					'domain' : current_site,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					})
			send_mail = EmailMessage(mail_subject, message, to=[email])
			print(send_mail)
			send_mail.send()
			messages.success(request, 'A reset link sent to your email')
			return redirect('login')
		else:
			messages.error(request, 'Email Does Not Exist')
			return redirect('password_reset')


class PasswordResetEmailView(View):

	def get(self,request, uidb64, token, *args, **kwargs):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = CustomUser.objects.get(pk=uid)

		except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
			user = None
		if user is not None and default_token_generator.check_token(user, token):
			request.session['uid'] = uid
			messages.success(request, 'Please Reset Your Password')
			return redirect('create_new_password')
		else:
			messages.error(request, 'Something went wrong, please try again later')
			return redirect('login')



class CreateNewPasswordView(View):
	def get (self, request, *args, **kwargs):
		return render(request, 'accounts/create_new_password.html')
		
	def post(self, request, *args, **kwargs):
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')

		if password == confirm_password:
			uid = request.session.get('uid')
			user = CustomUser.objects.get(pk=uid)
			user.set_password(password)
			user.save()
			messages.success(request, 'Password Reset Successfully. Please Login with new password')
			return redirect('login')
		else:
			messages.error(request, 'Password Does Not Match')
			return redirect('create_new_password')


class AccountCreatedView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/account_created.html')


class AccountVerifiedView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/account_verified.html')
