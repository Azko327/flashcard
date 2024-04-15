# cards/templatetags/cards_tags.py

from django import template

from cards.models import Card

register = template.Library()

@register.inclusion_tag("cards/box_links.html")
def boxes_as_links():
    boxes = [
        {"number": 1, "name": "Need to repeat", "card_count": Card.objects.filter(box=1).count()},
        {"number": 2, "name": "Learned", "card_count": Card.objects.filter(box=2).count()},
    ]
    return {"boxes": boxes}
