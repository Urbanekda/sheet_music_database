"""
URL configuration for sheet_music_database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
import sheet_music_app.views as views
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("sheet/add", views.add_sheet, name="add_sheet"),
    path('delete/<int:pk>/', views.delete_sheet, name='delete_book'),
    path("edit/<int:pk>", views.edit_sheet, name="edit_page"),
    path("book/<int:pk>", views.sheet_profile, name="sheet_profile"), 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page="home"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]
