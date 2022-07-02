from django.contrib.auth.models import Group
from auction.models import Seller, User
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_auction.settings')

django.setup()

# now add data

user = {
    'username': 'seller',
    'email': 'shivanshu@gmaill.com',
}
user, created = User.objects.get_or_create(**user)

if created:
    user.set_password('123')
    user.save()
    seller = {
        'user': user,
        'contact': '12345678',
        'address': 'india',
        'first_name': 'shivanshu123',
        'last_name': 'semwal',
    }
    seller, created = Seller.objects.get_or_create(**seller)
    Group.objects.get(name='sellers').user_set.add(user)
else:
    print('User already exists ' + str(user))
