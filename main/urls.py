"""mi1web URL Configuration

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
from . import views


app_name = 'main'

urlpatterns = [
    path('nuevo_product', views.AddProduct, name = 'Add_Product'),
    path('getProduccionFormset', views.GetProductionFormset, name = 'Get_Production_Formset'),
    path('nueva_produccion', views.NuevaProduccion, name = 'Nueva_Produccion'),
    path('nueva_FT', views.NuevaFT, name = 'Nueva_FT'),
    path('nuevo_traslado_emitido', views.NuevoTrasladoEmitido, name = 'Nuevo_Traslado_Emitido'),
    path('nuevo_vale', views.NuevoVale, name = 'Nuevo_Vale'),
    path('', views.MainFunc, name='Main_Page'),
    ]
