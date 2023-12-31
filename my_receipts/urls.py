"""
URL configuration for my_receipts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from receipts.views import home, page_not_found, user_register, user_login, user_logout

urlpatterns = [
    path('', home, name="home"),
    path('404/', page_not_found, name="page-not-found"),
    path('register/', user_register,  name="user-register"),
    path('login/', user_login,  name="user-login"),
    path('logout/', user_logout,  name="user-logout"),
    path('receipts/', include('receipts.urls')),
    path('admin/', admin.site.urls),
]
