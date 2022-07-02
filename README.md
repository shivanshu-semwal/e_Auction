# e-Auction System

## Technologies Used 

- [bootstrap v4.6](https://getbootstrap.com/docs/4.6/getting-started/build-tools/)
- [django v.4.0](https://docs.djangoproject.com/en/4.0/)
- [font awesome icons v6.1](https://fontawesome.com/search?s=solid%2Cbrands)
- [style guide for python](https://peps.python.org/pep-0008/)

## Setup

- Create python virtual environment - `python3 -m venv django`
- Activate the virtual environment - `source ./django/bin/activate` for linux
- Install the required modules in the `pip3 install -r requirements.txt`

## Run 

- `python manage.py runserver` - for running server
- `python manage.py makemigrations auction` - making migrations
- `python manage.py migrate` applying migrations to database
- `python manage.py createsuperuser` - create admin user

## Resources Used

- [change label in for](https://stackoverflow.com/questions/636905/django-form-set-label_)
- [upload only image](https://stackoverflow.com/questions/6460848/how-to-limit-file-types-on-file-uploads-for-modelforms-with-filefields)
- [frontend mime type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file)
- [django main admin site is messed up navigation bar](https://stackoverflow.com/questions/67709529/django-admin-site-nav-sidebar-messed-up)
- [multiple url files for django](https://stackoverflow.com/questions/59698254/how-do-i-create-multiple-urls-py-in-django-app)
- [bootstrap center items](https://stackoverflow.com/questions/39031224/how-to-center-cards-in-bootstrap-4)
- [bootstrap templates](https://mdbootstrap.com/docs/standard/extended/login/#!)
- [django default date field](https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date)
- [django delete models](https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models)
- https://stackoverflow.com/questions/11241668/what-is-reverse
- https://stackoverflow.com/questions/43179875/when-to-use-django-get-absolute-url-method
- https://stackoverflow.com/questions/11686007/font-awesome-input-type-submit
- https://freefrontend.com/bootstrap-product-cards/
- https://stackoverflow.com/questions/59408167/list-of-current-user-objects-in-django-listview
- https://stackoverflow.com/questions/34319752/how-to-raise-a-error-inside-form-valid-method-of-a-createview
- https://docs.djangoproject.com/en/4.0/ref/forms/api/#django.forms.Form.add_error
- https://docs.djangoproject.com/en/4.0/ref/models/querysets/#get
- https://docs.djangoproject.com/en/4.0/ref/forms/api/#django.forms.Form.add_error
- https://stackoverflow.com/questions/59124344/pass-pk-to-createview-form-in-django
- https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView
- https://stackoverflow.com/questions/51114608/how-to-create-an-object-inside-the-createview-in-django
- https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/
- https://docs.djangoproject.com/en/4.0/topics/db/queries/#:~:text=Creating%20objects&text=To%20create%20an%20object%2C%20instantiate,save%20it%20to%20the%20database.&text=This%20performs%20an%20INSERT%20SQL,method%20has%20no%20return%20value.
- https://stackoverflow.com/questions/13309479/django-createview-how-to-get-the-object-that-is-created
- https://stackoverflow.com/questions/21855357/how-to-add-indian-standard-time-ist-in-django
- https://chriskief.com/2012/12/30/django-class-based-views-with-multiple-forms/

# License

MIT