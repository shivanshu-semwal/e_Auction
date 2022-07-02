import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_auction.settings')

import django
django.setup()

# now add data
from auction.models import User, Bidder
from django.contrib.auth.models import Group

user = {
    'username': 'bidder',

    'email': 'shivanshu@gmail.com',
}
user, created = User.objects.get_or_create(**user)

if created:
    user.set_password('123')
    user.save()
    bidder = {
        'user': user,
        'contact': '12345678',
        'address': 'india',
        'first_name': 'shivanshu',
        'last_name': 'semwal',
    }
    bidder, created = Bidder.objects.get_or_create(**bidder)
    Group.objects.get(name='bidders').user_set.add(user)
else:
    print('User already exists ' + str(user))

user = {
    'username': 'default',
}
user, created = User.objects.get_or_create(**user)

if created:
    user.set_password('123')
    user.save()
    bidder = {
        'user': user,
    }
    bidder, created = Bidder.objects.get_or_create(**bidder)
    Group.objects.get(name='bidders').user_set.add(user)
else:
    print('User already exists ' + str(user))