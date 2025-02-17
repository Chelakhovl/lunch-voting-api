from restaurants.models import Menu
from django.utils.timezone import now


def get_voting_results(date=None):
    """
    Fetch voting results for a given date.
    Defaults to today's date if not provided.
    """
    date = date or now().date()
    menus = Menu.objects.filter(date=date).prefetch_related("votes")

    results = [
        {
            "restaurant": menu.restaurant.name,
            "menu_id": menu.id,
            "votes": menu.votes.count(),
        }
        for menu in menus
    ]

    return sorted(results, key=lambda x: x["votes"], reverse=True)
