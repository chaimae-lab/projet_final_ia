"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include  # Assure-toi que include est bien importé !
#from voyage.views import recuperer_plan_voyage
from voyage.views import home
from voyage.views import delete_account
from voyage.views import delete_data_view

from voyage.views import FacebookLogin
from voyage.views import GoogleLoginAPIView
#a suppri
#from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

#from dj_rest_auth.registration.views import SocialLoginView

#class FacebookLogin(SocialLoginView):
   # adapter_class = FacebookOAuth2Adapter


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('voyage.url_voyage')),  # Lien vers voyage/url_voyage.py
    path('accounts/', include('allauth.urls')),  #  # Redirection Facebook

    path('', home, name='home'), 

    
    path('auth/', include('dj_rest_auth.urls')),  # login/logout endpoints
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # inscription
    

    
    path('api/delete-user/', delete_account),  #delete data 
    path('delete-data/', delete_data_view, name='delete_data'),#delete data app dev
   
   # path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'), #facebook
    path('auth/facebook-login/', FacebookLogin.as_view(), name='fb_login'), #facebook auth
    path('api/google-login/', GoogleLoginAPIView.as_view(), name='google-login'),#google auth



]

