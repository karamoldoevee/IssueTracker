from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Profile


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    email = forms.CharField(label='Email', required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise ValidationError("Такой пользователь уже есть", code='username_taken')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise ValidationError("Эта почта уже используется", code='email_taken')
        except User.DoesNotExist:
            return email

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if not (first_name or last_name):
            raise ValidationError('Имя или фамилия не должно быть пустым!', code ='first_or_last_name_required')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия'}


class UserChangeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    birth_date = forms.DateField(label='День рождения', input_formats=['%Y-%m-%d','%d.%m.%Y'], required=False)
    link = forms.URLField(max_length=256, required=False, label = 'Ссылка на гитхаб', widget=forms.URLInput)
    about_me = forms.CharField(max_length=512, required=False, label='О себе',
                               widget=forms.Textarea)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field,field_name)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'birth_date', 'link', 'about_me']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}
        profile_fields = ['avatar', 'birth_date', 'link', 'about_me']

    def save(self, commit=True):
        user = super().save(commit)
        self.save_profile(user)
        return user

    def save_profile(self, user, commit=True):
        profile = Profile.objects.get_or_create(user=user)[0]
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if commit:
            profile.save()

    def clean_link(self):
        link = self.cleaned_data['link']
        if not ('github.com' in link):
            raise ValidationError('Это не ссылка на гитхаб!', code='not_github_link')
        return link


class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True, label='Новый пароль',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='Подтвердите новый пароль',
                                       widget=forms.PasswordInput)
    old_password = forms.CharField(max_length=100, required=True, label='Старый пароль',
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError('Invalid password.', code='invalid_password')
        return old_password

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match.', code='passwords_do_not_match')
        return self.cleaned_data

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']