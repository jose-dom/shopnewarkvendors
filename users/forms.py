from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Profile, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    
    class Meta:
        model = User
        fields = [
            'company_name', 'legal_name', 'email', 'address', 'business_type', 'contact_name', 'phone_number', 'website',
            'bank_name', 'branch_location', 'aba_number', 'account_number',
            'banner',
            'business_structure', 'length_of_operation', 'number_of_employees', 'location_type', 'speical_business',
            'tax_credits',
            'terms_conditions',
            'password1', 'password2'
        ]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['address', 'website', 'email', 'phone_number']

class SpecialUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'company_name', 'legal_name', 'business_type', 'contact_name',
            'business_structure', 'length_of_operation', 'number_of_employees', 'location_type', 'speical_business',
            'tax_credits',
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")
