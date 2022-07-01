from django.contrib import admin
from django.urls import path, re_path, include
from auction.views import basic, register, admins, bidder, seller

# https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
from django.conf import settings
from django.conf.urls.static import static

register_url = [
    re_path(r"^$", register.register, name='register'),
    re_path(r"new_auction_admin", register.create_auction_admin,
            name='new_auction_admin'),
    re_path(r"new_auction_user", register.create_auction_seller,
            name='new_auction_user'),
    re_path(r"new_auction_bidder", register.create_auction_bidder,
            name='new_auction_bidder'),
]

admins_url = [
    re_path(r"^$", admins.admin_home),
    path("home/", admins.admin_home, name='admin_home'),
    path("profile/", admins.admin_profile, name='admin_profile'),
    re_path(r"categories/$", admins.CategoriesListView.as_view(), name='view_categories'),
    re_path(r"^categories/(?P<pk>\d+)/$", admins.CategoriesDetailView.as_view(), name="category_detail"),
    re_path(r"^categories/add$", admins.CategoriesCreateView.as_view(), name='add_categories'),
    re_path(r"^categories/update/(?P<pk>\d+)/$", admins.CategoriesUpdateView.as_view(), name="category_update"),
    re_path(r"^categories/delete/(?P<pk>\d+)/$", admins.CategoriesDeleteView.as_view(), name="category_delete"),
]

seller_url = [
    path("home/", seller.seller_home, name='seller_home'),
    path("profile/", seller.seller_profile, name='seller_profile'),
    path("products/", seller.ProductListView.as_view(), name='view_products'),
    path("products/create/", seller.ProductCreateView.as_view(), name='add_product'),
    re_path(r"products/(?P<pk>\d+)/$", seller.ProductDetailView.as_view(), name='product_detail'),
]

bidder_url = [
    path("home/", bidder.bidder_home, name='bidder_home'),
    path("profile/", bidder.bidder_profile, name='bidder_profile'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", basic.index, name='index'),
    path("about/", basic.about_us, name='about'),
    path("login/", basic.login_user, name='login_user'),
    path("logout/", basic.logout_user, name='logout_user'),
    re_path(r"^register/", include(register_url)),
    re_path(r"^admins/", include(admins_url)),
    re_path(r"^seller/", include(seller_url)),
    re_path(r"^bidder/", include(bidder_url)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
