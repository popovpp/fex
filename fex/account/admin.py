from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.forms import CustomUserCreationForm, CustomUserChangeForm

from account.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'show_groups',
                    'is_active', 'is_staff', 'balance', 'freeze_balance')
    list_filter = ('email', 'groups', 'is_active',)
    fieldsets = ((None, {'fields': ('email', 'password', 'first_name', 'last_name',)}),
                ('Permissions', {'fields': ('groups', 'is_active')}),)
    add_fieldsets = ((None, {'classes': ('wide',),
                    'fields': ('email', 'password1', 'password2', 'first_name', 
                    'last_name', 'groups', 'is_active')}),)
    search_fields = ('email',)
    ordering = ('email',)

    def show_groups(self, obj):
    	return ", ".join([a.name for a in obj.groups.all()])


admin.site.register(User, CustomUserAdmin)
