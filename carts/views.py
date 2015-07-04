from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, Http404, HttpResponseRedirect
from django.core.context_processors import csrf
# Create your views here.
from .models import Cart, CartItem
from products.models import Product, ProductVariation
from .utils import *

def view(request):
	c = get_base_context(request)
	try:
		the_id = request.session['cart_id']
	except:
		the_id = None
	#cart = Cart.objects.all()[0]
	if the_id:
		cart = Cart.objects.get(id=the_id)
		c.update({"cart": cart})
	else:
		c.update({"cart_empty": True, "message": "Your Cart is empty, please keep shopping."})

	#show total on view
	new_total = 0.00
	for item in cart.cartitem_set.all():
		line_total = float(item.product.price)*item.quantity
		new_total += line_total

	request.session['cart_items_total'] = cart.cartitem_set.count()
	print cart.cartitem_set.count()
	cart.total = new_total
	cart.save()

	template = 'cart/view.html'
	return render_to_response(template, c)

def remove_from_cart(request, id):
	print "im here, delete me"
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse('cart'))

	cart_item = CartItem.objects.get(id=id)
	#remove cart item or update with quantity if qty passed to the view.
	#cart_item.delete()

	#or just make the cart in cart item empty so we store what users have in their carts
	cart_item.cart = None
	cart_item.save()

	#send success message
	return HttpResponseRedirect(reverse('cart'))

def add_to_cart(request, slug):
	#set time out for cart session
	request.session.set_expiry(30000000)

	try:
		the_id = request.session['cart_id']
	except:
	 	#create new cart session
	 	new_cart = Cart.objects.create(active=True)
	 	new_cart.save()
	 	request.session['cart_id'] = new_cart.id
	 	the_id = new_cart.id
	
	#cart unique to session
	cart = Cart.objects.get(id=the_id)

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass

	#Getting prod variations with Get
	'''try:
		qty = request.GET.get('qty')
		update_qty = True
	except:
		qty = None
		update_qty = False

	notes = {}

	try:
		color = request.GET.get('color')
		notes['color'] = color
	except:
		color = None

	try:
		size = request.GET.get('size')
		notes['size'] = size
	except:
		size = None '''

	#get list of product variations
	product_var = []
	#Get form post data
	if request.method == "POST":
		qty = request.POST.get('qty')
		#if int(qty) <= 0
		for post in request.POST:
			key = post
			val = request.POST[key]
			# print key, val
			try:
				#get instance of product variation to enter results of post
				v = ProductVariation.objects.get(product=product, category__iexact=key, title__iexact=val) #iexact ignores upper or lowercase
				product_var.append(v)
			except:
				pass

		#add cart item info. Unique only to product
		#cart_item, created = CartItem.objects.get_or_create(cart=cart, product = product) 
		#above line equates to tuple (model object, "true/false")
		cart_item = CartItem.objects.create(product=product, cart=cart)

		#remove cart item or update with quantity if qty passed to the view.
		#cart_item.delete()
		#clear out previous variations before adding new ones
		#cart_item.variations.clear()
		#add variation to cart
		if len(product_var) > 0:
			for item in product_var:
				cart_item.variations.add(item)

			#Alternative way of adding for loop to manytomany field
			#cart_item.vartiation.add(*item)

		#cart_item.notes = notes #save notes into cart notes field
		cart_item.quantity = qty
		cart_item.save()

		return HttpResponseRedirect(reverse("cart"))
	
	return HttpResponseRedirect(reverse("cart"))
