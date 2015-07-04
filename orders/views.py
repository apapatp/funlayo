from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.core.context_processors import csrf
from .utils import *
from carts.models import Cart

# Create your views here.
def checkout(request):
	#get cart data
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id = the_id)
	except:
		the_id = None

	c = get_base_context(request)
	template = "orders/checkout.html"
	return render_to_response(template, c)