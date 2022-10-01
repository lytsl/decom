from django import forms
from django.core import validators

from accounts.models import Account


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Name', help_text='Name is required', max_length=50, required=True)
    email = forms.EmailField(label='Email', error_messages={'validate': 'Valid email is required'},
                             validators=[validators.EmailValidator(message="Invalid Email")], required=True,
                             )
    phone_num = forms.CharField(label='Phone Number', help_text='Phone Number is required', required=True)
    password = forms.CharField(label='Password', help_text='Password is required', required=True,
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', help_text='Password is required', required=True,
                                       widget=forms.PasswordInput())

    # class Meta:
    #     model = Account
    #     fields = ['name', 'phone_num', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")

        if email and Account.objects.filter(email=email).exists():
            raise forms.ValidationError("An account already exist with this email address. Try Logging In")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'input100'
