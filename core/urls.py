"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from posts.views import signup_view, login_view, posts_list_create, post_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup_view),
    path('api/login/', login_view),
    
   
    path('api/posts/', posts_list_create), 
    path('api/create-post/', posts_list_create), 
    
    path('api/posts/<int:pk>/', post_detail),
]