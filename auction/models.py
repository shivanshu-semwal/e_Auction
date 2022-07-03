from webbrowser import get
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone

"""Models for the auction system"""

UPDATE_REF = "just a reference for updating balance"


class Bidder(models.Model):
    """User: Bidder who will post the items to bid on"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='bidder')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    balance = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username


class Seller(models.Model):
    """User: Auction User who will bid on the items"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='seller')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    balance = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username


class AdminUser(models.Model):
    """User: Auction User who will bid on the items"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """Main Category of the product"""
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})


class AuctionedProduct(models.Model):
    bid_id = models.IntegerField(null=False, default=-1)
    amount = models.IntegerField()
    bidder = models.ForeignKey(
        Bidder, on_delete=models.CASCADE, related_name='auctioned_product')


class Product(models.Model):

    STATUS_CHOICES = [
        ('FAILED', 'Not Sold'),
        ('SUCCESS', 'Sold'),
    ]

    creator = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    min_price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='items_pics/', null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='products')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=False)
    auctioned = models.OneToOneField(
        AuctionedProduct, on_delete=models.CASCADE, related_name='product')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)

    @property
    def isActive(self):
        return (timezone.now() < self.end_time) and (timezone.now() > self.start_time)

    @property
    def getStatus(self):
        if self.status:
            return self.status
        elif self.isActive:
            return "RUNNING"
        elif timezone.now() < self.start_time:
            return "NOT_STARTED"
        else:
            # set the status
            current = Product.objects.get(pk=self.pk)
            if self.auctioned.bidder.user.username == 'default':
                current.bidder = User.objects.get(username='dead').bidder
                current.status = "FAILED"
            else:
                # get the bid which won and set its status
                models.UPDATE_REF = "ref 2 - won bid"
                bid = Bid.objects.get(
                    bidder=current.auctioned.bidder, amount=self.auctioned.amount, product=self)
                bid.status = "SUCCESS"
                bid.save()
                current.status = "SUCCESS"
                c = Seller.objects.get(pk=current.creator.pk)
                c.balance = c.balance + bid.amount
                c.save()
            current.save()
            return current.status

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def clean(self) -> None:
        if self.start_time > self.end_time:
            raise ValidationError('Start Time should be less than end Time')
        return super().clean()

    def __str__(self):
        # "From: " + self.start_time.strftime('%Y-%m-%d %H:%M') + " To: " + self.end_time.strftime('%Y-%m-%d %H:%M')
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(start_time__lte=F('end_time')),
                name='start_before_end'
            )
        ]


class Bid(models.Model):
    STATUS_CHOICES = [
        ('FAIL', 'failed'),
        ('SUCCESS', 'success'),
    ]
    amount = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(
        Bidder, on_delete=models.CASCADE, related_name='bids')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, null=True)

    @property
    def getStatus(self):
        if self.status:
            return self.status
        else:
            if self.product.auctioned.bidder != self.bidder:
                models.UPDATE_REF = "ref 2 - add back to balance"
                current = Bid.objects.get(pk=self.pk)
                bidder = Bidder.objects.get(pk=current.bidder.pk)
                bidder.balance = bidder.balance + current.amount
                bidder.save()
                current.status = "FAIL"
                current.save()
                return current.status
            else:
                return "PENDING"


class Report(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)