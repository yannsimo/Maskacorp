from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class Artist(models.Model):
    name = models.CharField(max_length=100)
    stage_name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='artist/profiles/')
    slogan = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stage_name


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('snapchat', 'Snapchat'),
        ('twitter', 'Twitter/X'),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(max_length=50)  # classe CSS de l'icône
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.artist.stage_name} - {self.platform}"


class MusicPlatform(models.Model):
    PLATFORM_CHOICES = [
        ('spotify', 'Spotify'),
        ('apple_music', 'Apple Music'),
        ('deezer', 'Deezer'),
        ('soundcloud', 'SoundCloud'),
        ('youtube_music', 'YouTube Music'),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='music_platforms')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.artist.stage_name} - {self.platform}"


# Model pour les vidéos virales
class ViralVideo(models.Model):
    PLATFORM_CHOICES = [
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('snapchat', 'Snapchat'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='viral_videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)

    # Vidéo hébergée ou lien externe
    video_file = models.FileField(
        upload_to='videos/viral/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'webm'])]
    )
    video_url = models.URLField(blank=True)  # Pour vidéos externes (TikTok, YouTube, etc.)

    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True)

    # Statistiques
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    # Hashtags liés
    hashtags = models.CharField(max_length=200, blank=True)  # ex: "#RapAuTaff #KeshFamily"

    # Paramètres d'affichage
    is_featured = models.BooleanField(default=False)  # Pour mettre en avant
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at', 'order']
        verbose_name = "Vidéo virale"
        verbose_name_plural = "Vidéos virales"

    def __str__(self):
        return f"{self.title} - {self.platform}"


# Model pour les contenus audio
class AudioContent(models.Model):
    AUDIO_TYPES = [
        ('freestyle', 'Freestyle'),
        ('single', 'Single'),
        ('extract', 'Extrait'),
        ('demo', 'Démo'),
        ('remix', 'Remix'),
        ('feat', 'Featuring'),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='audio_contents')
    title = models.CharField(max_length=200)
    audio_type = models.CharField(max_length=20, choices=AUDIO_TYPES)
    description = models.TextField(blank=True)

    # Fichier audio
    audio_file = models.FileField(
        upload_to='audio/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac', 'm4a'])]
    )

    # Image de couverture
    cover_image = models.ImageField(upload_to='audio/covers/', blank=True)

    # Métadonnées
    duration = models.CharField(max_length=10, blank=True)  # ex: "3:45"
    bpm = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True)

    # Liens externes
    spotify_url = models.URLField(blank=True)
    apple_music_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    soundcloud_url = models.URLField(blank=True)

    # Statistiques
    plays_count = models.IntegerField(default=0)
    downloads_count = models.IntegerField(default=0)

    # Paramètres d'affichage
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at', 'order']
        verbose_name = "Contenu audio"
        verbose_name_plural = "Contenus audio"

    def __str__(self):
        return f"{self.title} ({self.audio_type})"


class Release(models.Model):
    RELEASE_TYPES = [
        ('single', 'Single'),
        ('album', 'Album'),
        ('ep', 'EP'),
        ('mixtape', 'Mixtape'),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='releases')
    title = models.CharField(max_length=200)
    release_type = models.CharField(max_length=20, choices=RELEASE_TYPES)
    cover_image = models.ImageField(upload_to='releases/covers/')
    release_date = models.DateField()
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)  # pour la section "Dernière nouveauté"
    spotify_url = models.URLField(blank=True)
    apple_music_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # Lien vers les contenus audio
    audio_contents = models.ManyToManyField(AudioContent, blank=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return f"{self.title} - {self.artist.stage_name}"


# Model BuzzContent pour inclure vidéos et audio
class BuzzContent(models.Model):
    CONTENT_TYPES = [
        ('comment', 'Commentaire'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
        ('stat', 'Statistique'),
        ('testimonial', 'Témoignage'),
        ('reaction', 'Réaction'),
        ('media', 'Média'),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='buzz_content')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Médias associés
    image = models.ImageField(upload_to='buzz/', blank=True)
    video_url = models.URLField(blank=True)
    audio_file = models.FileField(
        upload_to='buzz/audio/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'm4a'])]
    )

    # Lien vers contenu viral ou audio
    related_viral_video = models.ForeignKey(ViralVideo, on_delete=models.CASCADE, blank=True, null=True)
    related_audio = models.ForeignKey(AudioContent, on_delete=models.CASCADE, blank=True, null=True)

    source = models.CharField(max_length=100, blank=True)  # ex: "TikTok", "Instagram"
    source_url = models.URLField(blank=True)

    # Statistiques du buzz
    engagement_count = models.IntegerField(default=0)  # likes, partages, commentaires

    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Contenu buzz"
        verbose_name_plural = "Contenus buzz"

    def __str__(self):
        return self.title


# Model pour les playlists
class Playlist(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='playlists/covers/', blank=True)

    # Contenus de la playlist
    audio_contents = models.ManyToManyField(AudioContent, through='PlaylistItem')

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    audio_content = models.ForeignKey(AudioContent, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['playlist', 'audio_content']

    def __str__(self):
        return f"{self.playlist.name} - {self.audio_content.title}"


# Model pour les réactions/commentaires sur les vidéos
class VideoComment(models.Model):
    viral_video = models.ForeignKey(ViralVideo, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_avatar = models.ImageField(upload_to='comments/avatars/', blank=True)
    comment_text = models.TextField()
    platform = models.CharField(max_length=20)
    original_url = models.URLField(blank=True)

    # Métadonnées
    likes_count = models.IntegerField(default=0)
    is_highlighted = models.BooleanField(default=False)  # Pour mettre en avant

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commentaire de {self.author_name} sur {self.viral_video.title}"


class Challenge(models.Model):
    name = models.CharField(max_length=100)
    hashtag = models.CharField(max_length=50)  # ex: #RapAuTaff
    description = models.TextField()
    video_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Lien vers les vidéos virales du challenge
    viral_videos = models.ManyToManyField(ViralVideo, blank=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    MESSAGE_TYPES = [
        ('booking', 'Booking'),
        ('collaboration', 'Collaboration'),
        ('media', 'Média'),
        ('other', 'Autre'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"


class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100, default="Kesh - Rap au Taff")
    meta_description = models.TextField(max_length=160)
    primary_color = models.CharField(max_length=7, default="#e50000")
    secondary_color = models.CharField(max_length=7, default="#ff6b00")
    contact_email = models.EmailField()
    analytics_code = models.TextField(blank=True)

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return self.site_title