"""web URL Configuration

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
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/abnormal_attack/', include('abnormal_attack.urls')),
    path('api/incident_response/', include('incident_response.urls')),
    path('api/risk_analysis/', include('risk_analysis.urls')),
    path('api/flow_monitoring/', include('flow_monitoring.urls')),
    path('asset-management/', include('asset_management.urls')),
    path('api/situation_prediction/', include('situation_prediction.urls')),
]
