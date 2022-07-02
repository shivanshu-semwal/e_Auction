import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_auction.settings')

import django
django.setup()

# now add data
from auction.models import User, AdminUser
from django.contrib.auth.models import Group

user = {
    'username': 'admin',
    'email': 'shi@gmail.com',
}
user, created = User.objects.get_or_create(**user)

if created:
    user.set_password('123')
    user.save()
    admin_user = {
        'user': user,
    }
    admin_user = AdminUser.objects.get_or_create(**admin_user)
    Group.objects.get(name='admins').user_set.add(user)
else:
    print('User already exists ' + str(user))