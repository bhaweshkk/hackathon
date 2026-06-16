from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/', views.mark_all_read, name='mark_all_read'),
    path('<int:user_pk>/', views.conversation, name='conversation'),
    path('team/<int:team_pk>/', views.team_chat, name='team_chat'),
]
