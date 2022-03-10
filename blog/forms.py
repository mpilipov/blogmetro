from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Comment
from django.contrib.auth import get_user_model

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
                                                                                        'class':'form-control',
                                                                                        'id':"inputUsername"
                                                                                    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
                                                                    'class': "form-control",
                                                                    'id': "InputPassword",
                                                                    }))
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
                                                                    'class': "form-control",
                                                                    'id': "ReInputPassword",
                                                                    }))
    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']
        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(
                "Такой пользователь уже существует, попробуйте ещё раз"
            )
    def save(self):
        entered_user = self.cleaned_data['username']
        print('UOA ', User.objects.all())
        print('EU ', entered_user)
        print("DDDD")
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        user.save()
        # сразу же авторизуем пользователя
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'id':'inputUsername'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control mt-2',
        'id':'inputPassword'
    }))


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class':'form-control',
        'id':'name',
        'placeholder':"Ваше имя"
    }))
    email = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={
        'class':'form-control',
        'id':'email',
        'placeholder':"Ваша почта"
    }))
    subject = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class':'form-control',
        'id':'subject',
        'placeholder':"Тема"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control md-textarea',
        'id':'message',
        'rows':2,
        'placeholder':"Ваше сообщение"
    }))


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                                            'class': 'form-control',
                                            'rows': 3
                                             }),
        }
