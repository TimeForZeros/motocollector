from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('motos/', views.motos_index, name='index'),
  path('motos/<int:moto_id>/', views.motos_detail, name='detail'),
  path('motos/create/', views.MotoCreate.as_view(), name='motos_create'),
  path('motos/<int:pk>/update/', views.MotoUpdate.as_view(), name='motos_update'),
  path('motos/<int:pk>/delete/', views.MotoDelete.as_view(), name='motos_delete'),
  # path('motos/<int:moto_id>/add_maintenance/', views.add_maintenance, name='add_maintenance'),
]