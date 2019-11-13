"""DatasetContributionSystem URL Configuration

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
from homepage import views as homepage_views
from user import views as user_views
from dataset import views as dataset_views

urlpatterns = [
    path('', homepage_views.index),
    path('admin/', admin.site.urls),
    path('login/', user_views.login_view), 

    path('dataset/', dataset_views.index),
    path('dataset/create/', dataset_views.create),
    path('dataset/<str:datasetname>/', dataset_views.show),
    path('dataset/<str:datasetname>/download/', dataset_views.download),

    path('logout/', user_views.logout_view), 
    path('signup/', user_views.signup_view), 
    path('profile/', user_views.profile_view), 
]
