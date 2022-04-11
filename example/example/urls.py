"""example URL Configuration

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
# Third Party Stuff
from django.contrib import admin
from django.urls import path
from django_google_integrations.apis import GoogleAuthViewSet
from rest_framework import routers

default_router = routers.DefaultRouter(trailing_slash=False)

# using google integration library viewset
default_router.register("api/auth/google", GoogleAuthViewSet, basename="google-auth")

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += default_router.urls
