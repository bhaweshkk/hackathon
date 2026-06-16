from django.urls import path
from . import views

app_name = 'hackathons'

urlpatterns = [
    path('', views.hackathon_list, name='list'),
    path('create/', views.hackathon_create, name='create'),
    path('<int:pk>/', views.hackathon_detail, name='detail'),
    path('<int:pk>/apply/', views.apply_hackathon, name='apply'),
    path('<int:pk>/bookmark/', views.toggle_bookmark, name='bookmark'),
]
