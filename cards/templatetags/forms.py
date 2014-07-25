

from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from cards.models import Player


__author__ = 'Arno'

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Player
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "phone")

    def clean_username(self):
            # Since User.username is unique, this check is redundant,
            # but it sets a nicer error message than the ORM. See #13147.
            username = self.cleaned_data["username"]
            try:
                Player.objects.get(username=username)
            except Player.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )