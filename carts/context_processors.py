from django.contrib.auth.models import AnonymousUser
from django.conf import settings as app_settings
from .models import *

import datetime

def init(request):
    cart_total = request.session.get('cart_items_total', None)

    context = {
        "cart_total": cart_total,
    }
    return context
