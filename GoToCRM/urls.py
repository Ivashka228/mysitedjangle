"""GoToCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from crm.views import *
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('student', details),
    path('courses', courses),
    path('course', detailscourse),
    path('add', add),
    path('addcourse', addcourse),
    path('edit', edit),
    path('editcourse', editcourse),
    path('delete', delete),
    path('deletecomment', deletecomment),
    path('deletecourse', deletecourse),
    path('register', register),
    path('login', login_page),
    path('logout', logout_page),
    path('comments', comments),
    path('comment', comment),
] + static('avatars/', document_root='avatars/')
