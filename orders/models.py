from django.db import models
from carts.models import Cart
from .constant import STATUS_CHOICES

# Create your models here.
class Order(models.Model):
	cart = models.ForeignKey(Cart)
	completion_status = models.CharField(max_length=120, choices = STATUS_CHOICES, default="Started")
	date_created = models.DateTimeField(auto_now_add=True, auto_now = False)
	date_modified = models.DateTimeField(auto_now_add=False, auto_now = True)
	generated_order_id = models.CharField(max_length=120, default="QWERTY", unique=True)
	#user
	#address

	class Meta:
		verbose_name = "order"
		verbose_name_plural = "orders"

	def __unicode__(self):
		return self.generated_order_id