"""ONE-2 authentication routes. Docs: docs/Requirements.md, docs/Spec.md."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from core.forms import AttendanceAuthenticationForm
from core.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="core/login.html",
            authentication_form=AttendanceAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("", home, name="home"),
]
