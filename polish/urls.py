"""polish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from polish.views import signup, validate_username, login, logout, welcome, main, home, lesson

urlpatterns = [
	url(r'^home/$', home),
	url(r'^$', main),
	url(r'^welcome/$', welcome),
	url(r'^signup/$', signup),
	url(r'^login/$', login),
	url(r'^logout/$', logout),
	url(r'^validate_username/$', validate_username),
	url(r'^api/lesson/$', lesson)
]
