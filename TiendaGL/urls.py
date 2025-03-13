"""
URL configuration for TiendaGL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from tiendaweb import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from tiendaweb.views import LoginSystem 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('productos/', views.productos, name="productos"),
    path('dproductos/<int:id>',views.dproductos, name="dproductos"),
    path('registro/', views.registro, name='registro'),
    path('venta/', views.venta, name='venta'),
    path("confirmar-venta/", views.confirmar_venta, name="confirmar_venta"),

    path('confirmar-venta/commit-pay/', views.commitpay, name="commit-pay"),

    path('administrador/', views.admin, name='administrador'),


    path('administrador/add', views.aproducto, name='aproducto'),
    path('administrador/adds', views.add_producto, name='add_producto'),
    path('administrador/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    path('administrador/cliente', views.acliente, name='acliente'),
    path('administrador/cliente/add', views.addcliente, name='addcliente'),
    path('administrador/cliente/adds', views.add_cliente, name='add_cliente'),
    path('administrador/cliente/eliminar/<str:cliente_rut>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('administrador/cliente/modificar/<str:cliente_rut>/', views.alterclientes, name='modificar_cliente'),
    path('administrador/cliente/modificar/<str:cliente_rut>/success', views.modclientes, name='mod_cliente'),

    
    path('buscar/',views.buscar, name='buscar'),
    path('administrador/boleta', views.boletas, name='boletas'),    
    path('login/', LoginSystem.as_view(), name='login'),
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
