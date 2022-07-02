from django.contrib import admin
from auction.models import Bidder, Seller, AdminUser, Report
from auction.models import Product, Category, Bid, AuctionedProduct

# Register your models here.
admin.site.register(Bidder)
admin.site.register(Seller)
admin.site.register(AdminUser)

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Bid)
admin.site.register(AuctionedProduct)
admin.site.register(Report)