from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('edit/', views.edit_profile, name='edit'),
    path('<int:pk>/', views.profile_detail, name='detail'),
]
