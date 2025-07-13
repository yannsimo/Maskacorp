from django.contrib import admin
from .models import (
    Artist,
    SocialLink,
    MusicPlatform,
    ViralVideo,
    AudioContent,
    Release,
    BuzzContent,
    Challenge,
    ContactMessage,
    SiteSettings,
    Playlist,
    PlaylistItem,
    VideoComment
)

# Configuration simple pour commencer
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['stage_name', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'stage_name']

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['artist', 'platform', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    ordering = ['order']

@admin.register(MusicPlatform)
class MusicPlatformAdmin(admin.ModelAdmin):
    list_display = ['artist', 'platform', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    ordering = ['order']

@admin.register(ViralVideo)
class ViralVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'views_count', 'likes_count', 'is_featured', 'is_active']
    list_filter = ['platform', 'is_featured', 'is_active', 'published_at']
    search_fields = ['title', 'description', 'hashtags']
    ordering = ['-published_at']

@admin.register(AudioContent)
class AudioContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'audio_type', 'plays_count', 'is_featured', 'is_active']
    list_filter = ['audio_type', 'is_featured', 'is_active', 'published_at']
    search_fields = ['title', 'description']
    ordering = ['-published_at']

@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_type', 'release_date', 'is_featured']
    list_filter = ['release_type', 'is_featured', 'release_date']
    ordering = ['-release_date']

@admin.register(BuzzContent)
class BuzzContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'source', 'engagement_count', 'is_active']
    list_filter = ['content_type', 'is_active', 'source']
    ordering = ['order', '-created_at']

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hashtag', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'hashtag']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message_type', 'created_at', 'is_read']
    list_filter = ['message_type', 'is_read', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'contact_email']

# Enregistrement simple pour les autres models
admin.site.register(Playlist)
admin.site.register(PlaylistItem)
admin.site.register(VideoComment)

# Configuration globale de l'admin
admin.site.site_header = "Administration Kesh"
admin.site.site_title = "Admin Kesh"
admin.site.index_title = "Gestion du site de Kesh"