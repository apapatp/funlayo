from django.conf.urls import patterns, include, url
from django.conf import settings #we are adding this here because of the staic files we changes around
from django.conf.urls.static import static #import static files due to our changes
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', "products.views.home", name="home"),
    url(r'^products/$', "products.views.products", name="products"),
    url(r'^s/$', "products.views.search", name="search"),
    url(r'^cart/$', "carts.views.view", name="cart"),
    url(r'^cart/(?P<id>\d+)/$', "carts.views.remove_from_cart", name="remove_from_cart"),
    url(r'^cart/(?P<slug>[\w-]+)/$', "carts.views.add_to_cart", name="add_to_cart"),
    #url(r'^products/(?P<all_items>.*)/$', "products.views.single", name="single_product")
    #url(r'^products/(?P<id>\d+)/$', "products.views.single", name="single_product"), #\d+ is for numbers in regex
    url(r'^checkout/$', "orders.views.checkout", name="checkout"),
    url(r'^products/(?P<slug>[\w-]+)/$', "products.views.single" ,name="single_product"),
    url(r'^admin/', include(admin.site.urls)),
) 

if settings.DEBUG:
	#if in development
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)#serving our static files. Dont forget to always run collect static after static folder change
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)