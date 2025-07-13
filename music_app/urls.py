from django.urls import path
from . import views

app_name = 'music_app'

urlpatterns = [
    # Page principale
    path('', views.landing_page, name='index'),

    # Contact
    path('contact/', views.contact_submit, name='contact_submit'),

    # APIs pour charger du contenu
    path('api/videos/', views.get_viral_videos, name='get_viral_videos'),
    path('api/audio/', views.get_audio_content, name='get_audio_content'),

    # Pages détaillées
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),

    # Tracking des clics
    path('track/<str:link_type>/<int:link_id>/', views.track_click, name='track_click'),
]