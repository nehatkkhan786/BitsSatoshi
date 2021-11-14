
# from django import forms
# from .models import CustomUser


# class CustomUserForm(forms.ModelForm):
# 	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
# 	class Meta:
# 		model = CustomUser
# 		fields = ['first_name', 'last_name', 'email', 'password','confirm_password']
# 		widgets = {

# 			'first_name': forms.TextInput(attrs={'class':'form-control'}),
# 			'last_name': forms.TextInput(attrs={'class':'form-control'}),
# 			'email': forms.EmailInput(attrs={'class':'form-control'}),
# 			'password':forms.PasswordInput(attrs={'class':'form-control'}),	

# 		}