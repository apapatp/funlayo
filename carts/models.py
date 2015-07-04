from django.db import models
from products.models import Product, ProductVariation

class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product,null=True, blank=True)
	quantity = models.IntegerField(default=1)
	variations = models.ManyToManyField(ProductVariation, null=True, blank=True)
	notes = models.CharField(max_length=50, null=True, blank=True)
	line_total = models.DecimalField(default=10.99, max_digits=100, decimal_places=2)
	date_created = models.DateTimeField(auto_now_add=True, auto_now = False)
	date_modified = models.DateTimeField(auto_now_add=False, auto_now = True)
	
	def __unicode__(self):
		try:
			return str(self.cart.id)
		except:
			return self.product.title

# Create your models here.
class Cart(models.Model):
	total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
	date_created = models.DateTimeField(auto_now_add=True, auto_now = False)
	date_modified = models.DateTimeField(auto_now_add=False, auto_now = True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return "Cart Id: %s" % (self.id)

	def __unicode__(self):
		return "Cart Id: %s" % (self.id)

	class Meta:
		verbose_name = "cart"
		verbose_name_plural = "carts"

