from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
        # fields = ('email', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_staff', 'is_active', 'groups', 'user_permissions')
