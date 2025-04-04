from django.contrib import admin
from django.urls import path
from sistema import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name ='index'),
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('segunda-pagina/', views.segunda_pagina, name='segunda_pagina'),
]
