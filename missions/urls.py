"""
URL configuration for missions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import os

from django.contrib import admin
from django.urls import path, include, re_path
from dotenv import load_dotenv
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView

load_dotenv()

schema_view = get_schema_view(
    openapi.Info(
        title="UR In-country Missions API",
        default_version='v1',
        description="API for the management of UR in-country missions",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="p.mutanguha@ur.ac.rw"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    url=os.environ.get('SWAGGER_URL')
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenObtainPairView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),


    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]
