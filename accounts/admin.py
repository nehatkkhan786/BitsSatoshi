from django.contrib import admin
from .models import Profile

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name' , 'last_name', )



class CustomUserAdmin(UserAdmin):
    readonly_fields = ["date_joined", "last_login"]
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username',  'email', 'password1', 'password2', ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)