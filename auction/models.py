from tkinter import CASCADE
from turtle import Turtle
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q, F
from django.urls import reverse
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
    STATUS_CHOICES = [
        ('FAIL', 'Failed'),
        ('SUCCESS', 'Sold'),
        ('ACTIVE', 'Under Bidding'),
        ('INACTIVE', 'Bidding not Started')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='INACTIVE')
    amount = models.IntegerField()
    bidder = models.ForeignKey(
        Bidder, on_delete=models.CASCADE, related_name='auctioned_product')


class Product(models.Model):
    creator = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    min_price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='items_pics/', null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='products')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=False, validators=[])
    auctioned = models.OneToOneField(
        AuctionedProduct, on_delete=models.CASCADE, related_name='product')

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
        ('PENDING', 'pending'),
    ]
    amount = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(
        Bidder, on_delete=models.CASCADE, related_name='bids')
    price = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')