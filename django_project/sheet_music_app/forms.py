from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Vyžadováno. Zadejte platnou emailovou adresu.')

    # Custom validation to ensure email is unique
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Emailová adresa je již používána.")
        return email

    class Meta:
        model = User
        fields = ('username', "email", 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(label='Nové heslo', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Potvrďte nové heslo', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Hesla se neshodují.")
        
        return cleaned_data

    def save(self, user, commit=True):
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user