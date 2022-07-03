import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_auction.settings')

import django
django.setup()

from auction.models import Category
# now add data

categories = ['Vehicle', 'Books', 'Others', 'Stationary', 'Toys']
descriptions = [
    'All product related to vehicles!',
    'All products related to books and reading materials!',
    'If your category is not present use this!',
    'All products related to stationary items like pen, color pencil, etc.',
    'Your unique toys goes here!'
]

for i in range(len(categories)):
    category = categories[i]
    description = descriptions[i]
    category, created = Category.objects.get_or_create(
        name=category, description=description)
    if not created:
        print('Duplicate category: ' + str(category))
