"""experiments_os URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #实验室管理
    path('pcr/list/', views.pcr_list),
    path('pcr/add/', views.pcr_add),
    path('echart/list/', views.echart_list),
    # path('echart/bar/',echart_bar),
    path('echart/sample/', views.echart_sample),
    path('echart/two/', views.echart_two),
    path('echart/one/', views.echart_one),
    path('echart/three/', views.echart_three),
    path('echart/four/', views.echart_four),
    path('echart/five/', views.echart_five),
    path('echart/six/', views.echart_six),
#抗体
    path('kangti/echart/',views.kangti_echart),
    path('kangti/echart/one/',views.kangti_echart_one),
    path('kangti/echart/two/',views.kangti_echart_two),
    path('kangti/echart/three/',views.kangti_echart_three)


]
