from django.core.urlresolvers import reverse #so we can pass urls to our templates
from django.db import models
from .constant import VAR_CATEGORIES

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField()
	price = models.DecimalField(decimal_places=2, max_digits = 100, default=30.00)
	sale_price = models.DecimalField(decimal_places=2, max_digits = 100, \
									null=True, blank=True)
	slug = models.SlugField(unique=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=True, auto_now = False)
	active = models.BooleanField(default=True)
	#image = models.FileField(null=True, blank=True, max_length=200, upload_to="products/images")

	class Meta:
		unique_together = ('title','slug')#make fields unique together
		verbose_name = "product"
		verbose_name_plural = "products"

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title
	
	def get_price(self):
		return self.price

	def get_absolute_url(self):
		return "/products/%s/" %(self.slug)
		#return reverse("single_product", kwargs = {"slug":self.slug})
	
class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to="products/images/", null=True, blank = True)
	featured = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	thumbnail = models.BooleanField(default=False)

	def __unicode__(self):
		return self.product.title

class ProductVariationManager(models.Manager):
	def all(self):
		return super(ProductVariationManager, self).filter(active=True)
	
	def sizes(self):
		return self.all().filter(active=True).filter(category='size')

	def colors(self):
		return self.all().filter(active=True).filter(category='color')

	def package(self):
		return self.all().filter(active=True).filter(category='package')


class ProductVariation(models.Model):
	product = models.ForeignKey(Product) 
	image = models.ForeignKey(ProductImage, null=True, blank=True)
	title = models.CharField(max_length=120)
	category = models.CharField(max_length=100, choices=VAR_CATEGORIES, default='size')
	price = models.DecimalField(decimal_places=2, max_digits = 100, null=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	#set up managers to get category variations into a custom queryset
	objects = ProductVariationManager()

	def __unicode__(self):
		return self.title
