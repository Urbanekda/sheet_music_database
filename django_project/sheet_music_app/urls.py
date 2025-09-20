from django.urls import path
from django.contrib import admin
import sheet_music_app.views as views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("sheet/add", views.add_sheet, name="add_sheet"),
    path('delete/<int:pk>/', views.delete_sheet, name='delete_sheet'),
    path("edit/<int:pk>", views.edit_sheet, name="edit_sheet"),
    path("noty/<int:pk>", views.sheet_profile, name="sheet_profile"), 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page="home"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]