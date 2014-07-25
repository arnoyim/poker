from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect

# Create your views here.
from cards.models import Card, WarGame
from cards.templatetags.forms import EmailUserCreationForm
from week4 import settings


def home(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'cards.html', data)

def club(request):
    facecard = ['jack', 'queen', 'king']

    data = {
        'cards':Card.objects.all(),
        'facecard': facecard
    }
    return render(request, 'clubs.html', data)

def card_filter(request):

    data = {
        'cards':Card.objects.all(),

    }
    return render(request, "card_filters.html", data )

def suit_filter(request):
    data = {
        'cards':Card.objects.all()
    }
    return render(request, "suit_type.html", data)

@login_required
def profile(request):
    return render(request, 'profile.html', {})

def deal5(request):
    data = {
        'cards':Card.objects.all()
    }
    return render(request, "deal5.html", data)

def faq(request):
    return render(request,"faq.html")

@login_required
def blackjack(request):
    cards = Card.objects.order_by('?')[:2]
    data = {
        'cards': cards
    }
    for card in cards:
       if card.rank == 'ace':
           user = request.user
           text_content = 'Keep at it! {}'.format(user.username)
           html_content = '<h2>{} {} lucky you!!!</h2> <div> you just got an ACE</div>'.format(user.first_name, user.last_name)
           msg = EmailMultiAlternatives("ACE!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
           msg.attach_alternative(html_content, "text/html")
           msg.send()

    return render(request, 'blackjack.html', data)

def poker(request):
    data = {'cards': Card.objects.order_by('?')[:5]}

    return render(request, 'poker.html', data)

def hearts(request):
    data = {'cards': Card.objects.filter(suit=Card.HEART)}

    return render(request,'heart.html', data)

def no_face(request):
    facecard = ['jack', 'queen', 'king']
    data = {'cards': Card.objects.exclude(rank__in= facecard)}
    return render (request,"no_face.html", data)

def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.email_user("Welcome!", "Thank you for signing up for our website.")
            text_content = 'Thank you for signing up for our website, {}'.format(user.username)
            html_content = '<h2>Thanks {} {} for signing up!</h2> <div>I hope you enjoy using our site {}</div>'.format(user.first_name, user.last_name, user.date_joined)
            msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect("profile")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required()
def war(request):
    cards = list(Card.objects.order_by('?'))
    user_card = cards[0]
    dealer_card = cards[1]

    result = user_card.get_war_result(dealer_card)
    WarGame.objects.create(result=result, player=request.user)
    records= WarGame.objects.filter(player=request.user)

    return render(request, 'war.html', {
        'user_cards': [user_card],
        'dealer_cards': [dealer_card],
        'result': result,
        'records':records
    })