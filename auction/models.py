from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone

"""Models for the auction system"""


class MemberFees(models.Model):
    """Fee: Every bidder have to pay this fees"""
    fee = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return self.fee


class Bidder(models.Model):
    """User: Bidder who will post the items to bid on"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='bidder')
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Seller(models.Model):
    """User: Auction User who will bid on the items"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='seller')
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    membership = models.ForeignKey(
        MemberFees, on_delete=models.CASCADE, blank=True, null=True)

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
                bids = Bid.objects.filter(bidder=current.auctioned.bidder)
                for bid in bids:
                    bid.status = "FAIL"
                    bid.save()
                bid = Bid.objects.get(
                    bidder=current.auctioned.bidder, amount=self.auctioned.amount)
                bid.status = "SUCCESS"
                bid.save()
                current.status = "SUCCESS"
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
                current = Bid.objects.get(pk=self.pk)
                current.status = "FAIL"
                current.save()
                return current.status
            else:
                return "PENDING"
