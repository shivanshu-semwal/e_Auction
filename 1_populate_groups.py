import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_auction.settings')

import django
django.setup()

from django.contrib.auth.models import Group

Group.objects.get_or_create(name='admins')
Group.objects.get_or_create(name='bidders')
Group.objects.get_or_create(name='sellers')