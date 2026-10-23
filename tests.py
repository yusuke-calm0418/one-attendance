"""ONE-1 smoke checks plus ONE-2 authentication and authorization tests.

Docs: docs/Requirements.md (F-01); docs/Spec.md (section 2).
"""

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse


class PublicLoginPageTests(SimpleTestCase):
    def test_login_page_renders_without_authentication(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ログインする")
        self.assertContains(response, 'lang="ja"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, "ユーザー名")
        self.assertNotContains(response, "ユーザーIDまたはメールアドレス")

    def test_initial_home_is_protected(self):
        response = self.client.get(reverse("home"))
        self.assertRedirects(
            response, f'{reverse("login")}?next={reverse("home")}',
            fetch_redirect_response=False,
        )

    def test_static_login_stylesheet_is_referenced(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "core/site.css")


class AuthFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test-member", password="StrongUnique!Pass9281"
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other-member", password="OtherStrong!Pass4832"
        )

    def test_valid_credentials_redirect_to_protected_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "test-member", "password": "StrongUnique!Pass9281"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue("_auth_user_id" in self.client.session)
        protected = self.client.get(reverse("home"))
        self.assertEqual(protected.status_code, 200)
        self.assertContains(protected, "test-member")
        self.assertContains(protected, "ログアウト")
        self.assertNotContains(protected, "other-member")
        self.assertContains(protected, "未実装")

    def test_invalid_credentials_show_error_without_logging_in(self):
        response = self.client.post(
            reverse("login"),
            {"username": "test-member", "password": "not-the-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ユーザー名またはパスワードが正しくありません")
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertNotContains(response, "not-the-password")

    def test_empty_form_shows_required_field_errors(self):
        response = self.client.post(reverse("login"), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ユーザー名")
        self.assertContains(response, "パスワード")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_next_parameter_returns_to_requested_protected_page(self):
        redirect = self.client.get(reverse("home"))
        response = self.client.post(
            reverse("login"),
            {
                "username": "test-member",
                "password": "StrongUnique!Pass9281",
                "next": reverse("home"),
            },
        )
        self.assertEqual(redirect.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_unsafe_external_next_is_rejected(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "test-member",
                "password": "StrongUnique!Pass9281",
                "next": "https://external.example/phishing",
            },
        )
        self.assertRedirects(response, reverse("home"))

    def test_logged_in_user_does_not_need_login_again(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("login")), reverse("home"))

    def test_logout_requires_post_and_removes_session(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertRedirects(
            self.client.get(reverse("home")),
            f'{reverse("login")}?next={reverse("home")}',
            fetch_redirect_response=False,
        )

    def test_logout_rejects_missing_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(reverse("logout"))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(client.get(reverse("home")).status_code, 200)

    def test_login_rejects_missing_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            reverse("login"),
            {"username": "test-member", "password": "StrongUnique!Pass9281"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertNotIn("_auth_user_id", client.session)

    def test_inactive_user_cannot_log_in(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        response = self.client.post(
            reverse("login"),
            {"username": "test-member", "password": "StrongUnique!Pass9281"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_admin_uses_django_authentication(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)


class DatabaseConnectionTests(TestCase):
    def test_postgresql_connection_responds(self):
        self.assertEqual(connection.vendor, "postgresql")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            self.assertEqual(cursor.fetchone(), (1,))
