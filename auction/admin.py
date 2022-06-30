from django.contrib import admin
from auction.models import Bidder, Seller, AdminUser
from auction.models import Product, Category

# Register your models here.
admin.site.register(Bidder)
admin.site.register(Seller)
admin.site.register(AdminUser)

admin.site.register(Category)

admin.site.register(Product)
