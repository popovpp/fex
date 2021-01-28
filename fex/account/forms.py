from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'groups', 'is_active',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'groups', 'is_active',)
