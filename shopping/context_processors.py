from store.models import Notification, SpecialOffer
from itertools import chain
from operator import attrgetter

def notifications_context(request):
    notifications = Notification.objects.filter(is_active=True)
    offers = SpecialOffer.objects.filter(is_active=True)

    # Tag each object with a type
    for n in notifications:
        n.type = "notification"
    for o in offers:
        o.type = "offer"

    # Combine and sort
    combined_feed = sorted(
        chain(notifications, offers),
        key=attrgetter('created_at'),
        reverse=True
    )

    return {
        'notifications': combined_feed[:5],
        'notifications_count': len(combined_feed)
    }
