from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.core.exceptions import ValidationError
from django import forms

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'type' ,'first_name','last_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class AccountAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ('email','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email',)
    readonly_fields=('id', 'date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'type' ,'first_name','last_name', 'password1', 'password2'),
        }),
    )
class RDVAdmin(admin.ModelAdmin):
    readonly_fields = ('date_RDV',)

# Register your models here.
admin.site.register(UserAccount, AccountAdmin)
admin.site.register(Citoyen)
admin.site.register(Centre)
admin.site.register(RDV, RDVAdmin)





