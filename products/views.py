from django.shortcuts import render, render_to_response, Http404
from django.conf import settings
from django.core.context_processors import csrf
from .models import Product
from carts.utils import get_base_context
from django.template import RequestContext

# Create your views here.
def home(request):
	c = get_base_context(request)
	products = Product.objects.all()
	c.update(
		{"products":products}
	)
	return render_to_response("products/home.html" , c)

def single(request, slug):
	#use try and exception blocks to avoid the debug page from showing and just raise exception
	#******* Problem with this from tutorial 20 - 22 not liking url passing for some reason ****#
	#try:
	product = Product.objects.get(slug=slug)
	images = product.productimage_set.all()
	#images = ProductImage.objects.filter(product=product)
	c = get_base_context(request)
	c.update({"product":product, "images":images})
	return render_to_response('products/single.html', c, context_instance=RequestContext(request))
	#except:
	#	raise Http404

def search(request):
	try:
		q = request.GET.get('q')
	except:
		q = None

	if q:
		products = Product.objects.all().filter(title__icontains=q) #icontains is a filter method of query set sort of like %% in sql
		c = get_base_context(request)
		c.update({'query':q, "products": products})
		template = 'products/results.html'
	else:
		c = get_base_context(request)
		template = 'products/home.html'
	return render_to_response(template, c)

def products(request):
	products = Product.objects.all()
	c = get_base_context(request)
	c.update({"products":products, "settings":settings.STATIC_ROOT})
	return render_to_response("products/products.html" , c)