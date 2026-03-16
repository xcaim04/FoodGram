from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import User


class RegisterForm(forms.ModelForm):
    """User registration form."""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mínimo 8 caracteres',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repite la contraseña',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'display_name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'tu@email.com', 'autocomplete': 'email'}),
            'username': forms.TextInput(attrs={'placeholder': '@usuario'}),
            'display_name': forms.TextInput(attrs={'placeholder': 'Tu nombre visible'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError('El nombre de usuario es obligatorio.')
        if username.startswith('@'):
            username = username[1:]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username.lower()

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Login form using email and password."""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'tu@email.com',
            'autocomplete': 'email',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Tu contraseña',
            'autocomplete': 'current-password',
        }),
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Email o contraseña incorrectos.')
            if not self.user.is_active:
                raise forms.ValidationError('Esta cuenta está desactivada.')
        return self.cleaned_data

    def get_user(self):
        return self.user


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile (email cannot be changed)."""

    class Meta:
        model = User
        fields = ['username', 'display_name', 'bio', 'avatar', 'location']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '@usuario'}),
            'display_name': forms.TextInput(attrs={'placeholder': 'Tu nombre visible'}),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos sobre ti y tu amor por la comida...',
                'rows': 3,
            }),
            'location': forms.TextInput(attrs={'placeholder': 'Ciudad, País'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if not username:
            raise forms.ValidationError('El nombre de usuario es obligatorio.')
        qs = User.objects.filter(username__iexact=username).exclude(email=self.instance.email)
        if qs.exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username


class ChangePasswordForm(forms.Form):
    """Form for changing the user's password."""
    current_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}),
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña (mín. 8 caracteres)'}),
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la nueva contraseña'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        pwd = self.cleaned_data.get('current_password')
        if not self.user.check_password(pwd):
            raise forms.ValidationError('La contraseña actual es incorrecta.')
        return pwd

    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password1')
        p2 = self.cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return p2

    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()
        return self.user
