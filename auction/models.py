from tkinter import CASCADE
from turtle import Turtle
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q, F

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
        User, on_delete=models.CASCADE, related_name='auction_user')
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
        User, on_delete=models.CASCADE, related_name='administrator')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """Main Category of the product"""
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.status


class Product(models.Model):
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, null=True, related_name='products')
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    min_price = models.IntegerField(null=True)
    images = models.ImageField(upload_to='items_pics/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name='products')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=False, validators=[])

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
