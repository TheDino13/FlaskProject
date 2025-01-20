from django.urls import path
from . import views

urlpatterns = [
    path('', views.language_list, name='language_list'),
    path('<int:language_id>/levels/', views.level_list, name='level_list'),
    path('<int:level_id>/details/', views.level_details, name='level_details'),
]
