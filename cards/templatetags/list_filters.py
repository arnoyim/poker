from django import template
import random
__author__ = 'Arno'

register = template.Library()

@register.filter
def suit (list, suit_type):
    return [item for item in list if item.get_suit_display() == suit_type]

@register.filter
def aces(list):
    return [item for item in list if item.rank == "ace"]

@register.filter
def rank(list, rank):
    return  [item for item in list if item.rank == rank]

@register.filter
def shuffle(cards):
    cards = list(cards)
    random.shuffle(cards)
    return cards

@register.filter
def deal(cards, amount):
    return cards[:amount]