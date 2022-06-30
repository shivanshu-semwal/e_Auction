import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_auction.settings')

import django
django.setup()

# now add data
from auction.models import Category

categories = ['Vehicle', 'Books', 'Others', 'Stationary', 'Toys']

for category in categories:
    category, created = Category.objects.get_or_create(name=category)
    if not created:
        print('Duplicate category: ' + str(category))