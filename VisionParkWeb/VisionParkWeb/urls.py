"""VisionParkWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from VisionParkWeb.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('edades/<int:edad>/<int:year>', calculaEdad),
    path('hereda/', hereda),
    path('manage/setup', setup),
    path('manage/edit/<int:id>', setup),
    path('manage/myparkings', my_parkings),
    path('about/', about),
    url(r'^signup/$', signup, name='signup'),
    path('manage/delete/<int:id>', parking_delete)
]
urlpatterns += staticfiles_urlpatterns()

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
