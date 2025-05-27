"""
URL configuration for quotes_project project.

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
from django.contrib import admin
from django.urls import path
from quotes_app import views as qv


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', qv.home, name='home'),
    path('login/', qv.login_view, name='login'),
    path('logout/', qv.logout_view, name='logout'),
    path('register/', qv.register_view, name='register'),
    path('add-author/', qv.add_author, name='add_author'),
    path('add-quote/', qv.add_quote, name='add_quote'),
    path('author/<int:pk>/', qv.author_detail, name='author_detail'),
    path('tag/<str:tag_name>/', qv.tag_quotes, name='tag_quotes'),
]
