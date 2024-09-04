from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from main.models import Profile

def get_trending_authors():
    one_week_ago = timezone.now() - timedelta(days=7)
    trending_authors = (
        Profile.objects.filter(user__article__view__viewed_at__gte=one_week_ago)
        .annotate(weekly_views=Count('user__article__view'))
        .order_by('-weekly_views')[:10]
    )
    return trending_authors