from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# Imports des models
from .models import (
    Artist,
    ViralVideo,
    AudioContent,
    Release,
    BuzzContent,
    Challenge,
    Playlist,
    SocialLink,
    MusicPlatform,
    ContactMessage,
    SiteSettings,
    VideoComment
)
from .forms import ContactForm


def landing_page(request):
    """Page d'accueil principale"""
    try:
        artist = Artist.objects.get(is_active=True)

        # Vidéos virales en vedette
        featured_videos = ViralVideo.objects.filter(
            artist=artist,
            is_featured=True,
            is_active=True
        ).order_by('order', '-published_at')[:6]

        # Contenus audio en vedette
        featured_audio = AudioContent.objects.filter(
            artist=artist,
            is_featured=True,
            is_active=True
        ).order_by('order', '-published_at')[:4]

        # Dernière sortie
        latest_release = Release.objects.filter(
            artist=artist,
            is_featured=True
        ).order_by('-release_date').first()

        # Buzz content
        buzz_content = BuzzContent.objects.filter(
            artist=artist,
            is_active=True
        ).order_by('order', '-created_at')[:6]

        # Challenges actifs
        challenges = Challenge.objects.filter(
            is_active=True
        ).order_by('-created_at')[:2]

        # Playlists
        playlists = Playlist.objects.filter(
            artist=artist,
            is_featured=True,
            is_active=True
        ).order_by('-created_at')[:3]

        # Liens sociaux et plateformes musicales
        social_links = SocialLink.objects.filter(
            artist=artist,
            is_active=True
        ).order_by('order')

        music_platforms = MusicPlatform.objects.filter(
            artist=artist,
            is_active=True
        ).order_by('order')

        # Paramètres du site
        site_settings = SiteSettings.objects.first()

        context = {
            'artist': artist,
            'featured_videos': featured_videos,
            'featured_audio': featured_audio,
            'latest_release': latest_release,
            'buzz_content': buzz_content,
            'challenges': challenges,
            'playlists': playlists,
            'social_links': social_links,
            'music_platforms': music_platforms,
            'site_settings': site_settings,
        }
        return render(request, 'music_app/index.html', context)  # ✅ Corrigé

    except Artist.DoesNotExist:
        return render(request, 'music_app/error.html', {  # ✅ Corrigé
            'error': 'Aucun artiste configuré',
            'message': 'Veuillez d\'abord créer un artiste dans l\'interface d\'administration.'
        })


def get_viral_videos(request):
    """API pour charger plus de vidéos virales"""
    page = request.GET.get('page', 1)
    platform = request.GET.get('platform', '')

    videos_query = ViralVideo.objects.filter(is_active=True)

    if platform:
        videos_query = videos_query.filter(platform=platform)

    videos_query = videos_query.order_by('-published_at')

    paginator = Paginator(videos_query, 12)  # 12 vidéos par page
    videos_page = paginator.get_page(page)

    data = []
    for video in videos_page:
        data.append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'thumbnail': video.thumbnail if video.thumbnail else '',
            'video_url': video.video_url,
            'platform': video.platform,
            'platform_display': video.get_platform_display(),
            'views_count': video.views_count,
            'likes_count': video.likes_count,
            'hashtags': video.hashtags,
            'published_at': video.published_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({
        'videos': data,
        'has_next': videos_page.has_next(),
        'has_previous': videos_page.has_previous(),
        'total_pages': paginator.num_pages,
        'current_page': videos_page.number,
    })


def get_audio_content(request):
    """API pour charger plus de contenus audio"""
    audio_type = request.GET.get('type', 'all')
    page = request.GET.get('page', 1)

    audio_query = AudioContent.objects.filter(is_active=True)
    if audio_type != 'all':
        audio_query = audio_query.filter(audio_type=audio_type)

    audio_query = audio_query.order_by('-published_at')

    paginator = Paginator(audio_query, 8)
    audio_page = paginator.get_page(page)

    data = []
    for audio in audio_page:
        data.append({
            'id': audio.id,
            'title': audio.title,
            'audio_type': audio.audio_type,
            'audio_type_display': audio.get_audio_type_display(),
            'duration': audio.duration,
            'cover_image': audio.cover_image if audio.cover_image else '',
            'audio_file': audio.audio_file.url if audio.audio_file else '',
            'spotify_url': audio.spotify_url,
            'plays_count': audio.plays_count,
        })

    return JsonResponse({
        'audio_content': data,
        'has_next': audio_page.has_next(),
        'total_pages': paginator.num_pages,
        'current_page': audio_page.number,
    })


@require_http_methods(["POST"])
def contact_submit(request):
    """Traitement du formulaire de contact"""
    try:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'message': 'Veuillez corriger les erreurs dans le formulaire.'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Une erreur est survenue. Veuillez réessayer plus tard.'
        })


def track_click(request, link_type, link_id):
    """Système de tracking des clics"""
    try:
        if link_type == 'social':
            try:
                social_link = SocialLink.objects.get(id=link_id)
                return JsonResponse({
                    'success': True,
                    'platform': social_link.platform,
                    'type': 'social'
                })
            except SocialLink.DoesNotExist:
                pass

        elif link_type == 'music':
            try:
                music_platform = MusicPlatform.objects.get(id=link_id)
                return JsonResponse({
                    'success': True,
                    'platform': music_platform.platform,
                    'type': 'music'
                })
            except MusicPlatform.DoesNotExist:
                pass

        elif link_type == 'video':
            try:
                video = ViralVideo.objects.get(id=link_id)
                # Incrémenter les vues
                video.views_count += 1
                video.save(update_fields=['views_count'])
                return JsonResponse({
                    'success': True,
                    'video_title': video.title,
                    'type': 'video'
                })
            except ViralVideo.DoesNotExist:
                pass

        elif link_type == 'audio':
            try:
                audio = AudioContent.objects.get(id=link_id)
                # Incrémenter les écoutes
                audio.plays_count += 1
                audio.save(update_fields=['plays_count'])
                return JsonResponse({
                    'success': True,
                    'audio_title': audio.title,
                    'type': 'audio'
                })
            except AudioContent.DoesNotExist:
                pass

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def video_detail(request, video_id):
    """Page détail d'une vidéo virale"""
    video = get_object_or_404(ViralVideo, id=video_id, is_active=True)
    comments = VideoComment.objects.filter(
        viral_video=video,
        is_highlighted=True
    ).order_by('-likes_count', '-created_at')[:10]

    # Incrémenter les vues (seulement si ce n'est pas un bot)
    if not request.META.get('HTTP_USER_AGENT', '').lower().startswith('bot'):
        video.views_count += 1
        video.save(update_fields=['views_count'])

    context = {
        'video': video,
        'comments': comments,
    }
    return render(request, 'music_app/video_detail.html', context)