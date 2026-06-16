from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from analytics import views as analytics_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analytics_views.landing, name='landing'),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('teams/', include('teams.urls')),
    path('hackathons/', include('hackathons.urls')),
    path('matching/', include('matching.urls')),
    path('messages/', include('messaging.urls')),
    path('dashboard/', include('analytics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
