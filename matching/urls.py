from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.recommendations, name='recommendations'),
    path('detail/<int:profile_pk>/', views.match_detail, name='detail'),
]
