from django import forms

from progame.models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if not user:
                raise forms.ValidationError({'email': ['Esse usuário não existe', ]})
            if not user.check_password(password):
                raise forms.ValidationError({'password': ['Senha incorreta', ]})
            if not user.is_active:
                raise forms.ValidationError('Esse usuário não é ativo')

        return cleaned_data


class CadastroForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirmar senha', required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            self.add_error('email', 'O email já está em uso')

        if password != confirm_password:
            self.add_error('confirm_password', 'As senhas não conferem')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome'
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean(self):
        instance = getattr(self, 'instance', None)
        cleaned_data = self.cleaned_data

        try:
            user = User.objects.get(email=cleaned_data.get('email'))
        except User.DoesNotExist:
            user = None

        if user and user.pk != instance.pk:
            self.add_error('email', 'O email já está em uso')

        return cleaned_data


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('imagem', )
        widgets = {
            'imagem': forms.FileInput
        }


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ('imagem', )
        widgets = {
            'imagem': forms.FileInput
        }