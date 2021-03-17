from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import *
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


def get_choices():
    array1 = list(Centre.objects.values_list('id', 'name'))
    return array1

class RegisteruserForm(forms.ModelForm):

    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)


    class Meta:
        model = UserAccount
        fields = ('email', 'password','first_name','last_name')
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserAccount.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email
class RegisterCitoyen(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
    phone=PhoneNumberField()
    class Meta:
        model=Citoyen
        fields=['address','CID','date_N','phone']

    def clean_CID(self):
        CID = self.cleaned_data['CID']
        if Citoyen.objects.filter(CID=CID).exists():
            raise forms.ValidationError('CID not Match')
        return CID
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if Citoyen.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Number phone already taken')
        return phone
class RDV_Register(forms.ModelForm):
    choice_field = forms.ChoiceField(widget=forms.Select, choices=get_choices(),required=True)
    is_cov19 = forms.BooleanField(required=False)
    ramid=forms.CharField(max_length=10)
    class Meta:
        model = RDV
        fields =('center_id',)


class UpdateUser(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('profile_image',)

    def save(self, commit=True):
        account = super(UpdateUser, self).save(commit=False)
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account
