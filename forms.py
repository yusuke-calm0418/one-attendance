"""ONE-2: presentation-only labels for Django's standard authentication form.

Docs: docs/Requirements.md (F-01), docs/Spec.md (section 2).
Authentication is by Django username, not by email; the email-login rule is TBD.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class AttendanceAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="ユーザー名",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "ユーザー名を入力",
                "class": "auth-input",
            }
        ),
    )
    password = forms.CharField(
        label="パスワード",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "パスワードを入力",
                "class": "auth-input",
            }
        ),
    )

    error_messages = {
        "invalid_login": _(
            "ユーザー名またはパスワードが正しくありません。入力内容を確認してください。"
        ),
        "inactive": _("このアカウントは無効です。管理者にお問い合わせください。"),
    }
