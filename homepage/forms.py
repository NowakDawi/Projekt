from django.forms import ModelForm
from .models import Movie
from .models import Comment
from django import forms
from django.contrib.auth.password_validation import password_validators_help_texts


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'genre', 'poster']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rate']

class CustomRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text=None
    )
    password2 = forms.CharField(widget=forms.PasswordInput)

    def get_password_help_texts(self):
        return password_validators_help_texts()