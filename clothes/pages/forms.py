from django import forms
# from .models import Member
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile, Category, Closet

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()  # auth.user
        fields = ('username',)

class ProfileForm(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '동/읍/면', 
                                                            'autocomplete':'off'}))
    class Meta:
        model = Profile
        fields = ('gender', 'region') 

class MultipleImageForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
