from django.contrib import admin
from .models import Product, ProductImage, ProductVariation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
	date_hierarchy = "timestamp"
	search_fields = ["title", "description"]
	list_display = ["__unicode__", "title","price", "timestamp", "updated", "active"]
	#edit things in the list display
	list_editable = ["price", "active"]
	#show filter menu
	list_filter = ["price", "active"]
	readonly_fields = ["timestamp","updated"]
	prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductVariation)