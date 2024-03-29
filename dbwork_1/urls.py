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
from dbapp.views import login,undergrade,postgraduate,chart
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login.login, name='login'), # 网站首页
    path('index/', views.login.index,name='index'),
    path('undergrade/list/', views.undergrade.undergrade_list),
    path('undergrade/add/', views.undergrade.undergrade_add),
    path('undergrade/edit/',views.undergrade.undergrade_edit),
    path('undergrade/detail/',views.undergrade.undergrade_detail),
    path('undergrade/upload/',views.undergrade.undergrade_upload),
    path('undergrade/delete/', views.undergrade.undergrade_delete),
    path('undergrade/deleteall/',views.undergrade.undergrade_deleteAll),
    path('test/', views.login.test),
    path('postgraduate/list/',views.postgraduate.postgraduate_list),
    #统计
    path('undergrade/chart/',views.undergrade.undergrade_chart),
    path('chart/bar/', undergrade.chart_bar),
    path('chart/pie/', undergrade.chart_pie),
    path('uchart/pie2/', undergrade.chart_pie2),
    path('postgraduate/list/', views.postgraduate.postgraduate_list),
    path('postgraduate/add/', views.postgraduate.postgraduate_add),
    path('postgraduate/edit/', views.postgraduate.postgraduate_edit),
    path('postgraduate/detail/', views.postgraduate.postgraduate_detail),
    path('postgraduate/upload/', views.postgraduate.postgraduate_upload),
    path('postgraduate/delete/',views.postgraduate.postgraduate_delete),
    path('postgraduate/deleteall/', views.postgraduate.postgraduate_deleteAll),
    # 统计
    path('postgraduate/chart/', views.postgraduate.postgraduate_chart),
    path('pchart/bar/', views.postgraduate.chart_bar),
    path('pchart/pie/', views.postgraduate.chart_pie),
    path('pchart/pie2/', views.postgraduate.chart_pie2),
]
