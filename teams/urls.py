from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='list'),
    path('create/', views.team_create, name='create'),
    path('<int:pk>/', views.team_detail, name='detail'),
    path('<int:pk>/edit/', views.team_edit, name='edit'),
    path('<int:pk>/leave/', views.leave_team, name='leave'),
    path('<int:team_pk>/invite/<int:user_pk>/', views.invite_member, name='invite'),
    path('invites/', views.my_invites, name='my_invites'),
    path('invites/<int:invite_pk>/<str:action>/', views.respond_invite, name='respond_invite'),
    path('connect/<int:user_pk>/', views.send_connection, name='connect'),
    path('connections/<int:conn_pk>/<str:action>/', views.respond_connection, name='respond_connection'),
]
