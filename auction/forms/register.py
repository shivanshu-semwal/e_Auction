from django import forms
from django.contrib.auth.models import User
from auction.models import Seller, Bidder


class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )

        return cleaned_data


class NewSellerForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput(),
                          required=False, label='Date of Birth')
    image = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/jpeg, image/png'}),
        required=False,
        label='Profile Image'
    )

    class Meta():
        model = Seller
        fields = ('first_name', 'last_name', 'dob', 'address', 'contact', 'image')


class NewBidderForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput(),
                          label='Date of Birth', required=False)
    image = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/jpeg, image/png'}),
        required=False,
        label='Profile Image'
    )

    class Meta():
        model = Bidder
        fields = ('first_name', 'last_name', 'dob', 'address', 'contact', 'image')
