from django.urls import path
from django.contrib import admin
import sheet_music_app.views as views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path("", views.home, name="home"),  # Main listing with filters + pagination
    path("sheet/add", views.add_sheet, name="add_sheet"),  # Create
    path('delete/<int:pk>/', views.delete_sheet, name='delete_sheet'),  # Delete
    path("edit/<int:pk>", views.edit_sheet, name="edit_sheet"),  # Update
    # Detail pages prefer slugs for stable, human-friendly URLs
    path("noty/<slug:slug>", views.sheet_profile, name="sheet_profile"),
    # Backwards compatibility: legacy integer-ID URLs redirect to slug version
    path("noty/id/<int:pk>", views.sheet_profile_redirect_by_pk, name="sheet_profile_by_pk"),
    path("noty/<int:pk>", views.sheet_profile_redirect_by_pk),
    # Auth views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page="home"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    # Password reset flow (Django's built-in views with custom templates)
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_complete"),
    # Static pages
    path("conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("privacy/", views.privacy_policy, name="privacy_policy"),
]