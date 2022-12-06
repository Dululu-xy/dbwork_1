"""dbwork_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from dbapp import views
from dbapp.views import login,undergrade,postgraduate
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login.login, name='login'), # 网站首页
    path('index/', views.login.index,name='index'),
    #本科生操作
    path('undergrade/list/', views.undergrade.undergrade_list),
    path('undergrade/add/', views.undergrade.undergrade_add),
    path('undergrade/edit/',views.undergrade.undergrade_edit),
    path('undergrade/detail/',views.undergrade.undergrade_detail),
    path('undergrade/upload/',views.undergrade.undergrade_upload),
    #研究生操作
    path('postgraduate/list/', views.postgraduate.postgrauate_list),
    path('test/', views.login.test),
]
