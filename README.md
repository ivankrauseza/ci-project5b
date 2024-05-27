# Code Institute - PP5 Version 2

# Sitemap
https://docs.google.com/document/d/1eg-6-Jtp0bN4qRNNa1RbKmSLPGvnc9nIOPRu5pCAiF4/edit?usp=sharing

# Identity Toolkit
## Google Font - Lato
https://fonts.google.com/specimen/Lato
## Colors
- [Color Scheme](https://www.canva.com/colors/color-palettes/colored-coolers/)


# Tests
## use sqlite for testing database:
```
if 'test' in os.environ.get('DJANGO_SETTINGS_MODULE', ''):
    # Use SQLite for tests
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
```

# Bugs
## AllAuth - python manage.py runserver
WARNINGS: account.EmailAddress: (models.W036) MySQL does not support unique constraints with conditions.
## Product Filtering and Sorting
Problem to filter by both brand and sort by price
## WARNINGS:
?: (templates.E003) 'custom_filters' is used for multiple template tag modules: 'erp.templatetags.custom_filters', 'shop.templatetags.custom_filters'


# Collectstatic


# Deployment
## Deployment to Heroku
- Create Procfile (web: gunicorn cadence.wsgi)
- Freeze requirements (pip freeze > requirements.txt)
- Create New Project
- Region: Europe 
- Setup Config Vars
- Deployment Method: GitHub > 'ci-project5b'
- Choose a branch to deploy 'main'
- Deploy Manually


# Media
Determine what systems to use to manage media files.


# References / Walkthrough / Credits
- [AllAuth Setup](https://docs.allauth.org/en/latest/installation/quickstart.html)
- [My Previous CI Project 4](https://github.com/ivankrauseza/ci-project4)
- [My Previous CI Project 5](https://github.com/ivankrauseza/ci-project5)
- Code Institute Walkthroughs: (Hello Django, I think therefore I blog, Boutique Ado)
- [Learning Django](https://www.linkedin.com/learning/learning-django-2/rapidly-create-web-applications)
- [MDN - Local Library](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website)
- [AWS S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
- [AWS S3 - Static Files](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/)
- [Django Stripe Integration](https://testdriven.io/blog/django-stripe-tutorial/)
- [robots.txt](https://learndjango.com/tutorials/add-robotstxt-django-website#:~:text=To%20implement%20a%20robots.,a%20new%20app%20called%20pages%20.&text=Immediately%20add%20it%20to%20your%20INSTALLED_APPS%20setting.&text=Then%20create%20a%20custom%20view,on%20the%20built%2Din%20TemplateView%20.)
- [404 and 500 error pages](https://learndjango.com/tutorials/customizing-django-404-and-500-error-pages)
- [Sitemap Generator](https://www.xml-sitemaps.com/)
- [About Us Stock Image](https://www.freepik.com/free-photo/brutal-tattooed-bearded-mechanic-specialist-repairs-car-engine-which-is-raised-hydraulic-lift-garage-service-station_28232164.htm#fromView=search&page=1&position=11&uuid=06f52f37-3676-447d-b125-76469a656364)

## Product Images
- [TE0123456789](https://www.jumia.com.ng/generic-mini-digital-multimeter-voltmeter-voltage-ampere-tester-160778516.html)
- [3456789012](https://naughtonfarmmachinery.ie/products/swampmaster-stormgear-waterproof-jacket)
- [0123456789](https://www.thegreekfoundation.com/shop/home/espresso-cup)