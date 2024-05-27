# Code Institute - PP5 Version 2
For my Project 5 at the Code Institute I have created an MVP e-commerce platform for a brand called Cadence Tools which sells tools. The platform is integrated with Stripe Checkout, and using MySQL for the Database and AWS S3 for file storage. The main aim of this project was to make the most of the default styles and functions offered by bootstrap. As this is a second attempt I decided to enhance the look and feel of the site with a different color scheme and rethinking how to structure the models, views and templates.

![Responsive Design - Powered by Bootstrap](https://cadence-v1.s3.eu-central-1.amazonaws.com/readme/ivankrause_cipp5b_responsive.png)

## Contents
- [Technology Stack](#technology-stack)
- [Identity Toolkit](#identity-toolkit)
- [User Experience](#user-experience)
- [Database Schema](#database-schema)
- [User Stories](#user-stories)
- [Setup](#setup)
- [Functionality](#functionality)
- [Deployment](#deployment)
- [Testing](#testing)
- [Bugs](#bugs)


# Technology Stack
See [requirements.txt](https://github.com/ivankrauseza/ci-project5/blob/main/requirements.txt) for an overview of the development environment.  
- Python (Django)
- HTML & CSS (Bootstrap @ 5.3.2)
- JavaScript (jQuery @3.7.1 and jQueryUI @ 1.13.2)
- Database (AWS - RDS)
- Media (AWS - S3)
- Stripe Checkout
- Icons FontAwesome @latest
- Markdown (ReadMe)


# Identity Toolkit
## Google Font - Lato
https://fonts.google.com/specimen/Lato

## Colors
- [CANVA Color Scheme](https://www.canva.com/colors/color-palettes/colored-coolers/)
- Orange #f6a21e
- Red Orange #e55b13
- Forest Green #104210
- Lime Green #7a871e


# User Experience
Taking inspiration from a previous role. I wanted to develop an updated, simple and cleaner e-commerce experience. I have also taken inspiration from IKEA to simplify the display and draw attention to the products right away and reduce distraction. Overall it is a standard e-commerce website that contains traditional user flow of Product List / Product Detail / Basket / Checkout but the User needs to register their account in order to add products to the basket. Users also have the basic tools to view previous orders and manage their account. I used Figma desktop app to wireframe and develop the protoype designs and color schemes:

## Wireframing and Prototype
![Figma](https://cadence-v1.s3.eu-central-1.amazonaws.com/readme/ivankrause_cipp5b_figma.png)


# User Stories
User stories were managed using GitHub Projects and Issues.
- [GitHub Projects and Issues](https://github.com/users/ivankrauseza/projects/4)

![User Stories](https://cadence-v1.s3.eu-central-1.amazonaws.com/readme/ivankrause_cipp5b_userstories.png)


# Functionality

## Database Schema
Using experience gained working in MS365 Dynamics NAV, I tried to replicate the database schema in it's simplest form to also structure the project in such a way that if it needed to be integrated into an ERP system that it would follow a similar approach.

## E-Commerce Platform
### Customers
Logged out customers can browse but need to have an account to add items to the basket and place orders.
### Admins
When logged in as an admin, a purple toobar loads at the top of the website with a link to access the ERP area to manage products and orders.
### Media
When uploading media, I have used Pillow to manage the resizing of larger images to reduce file size and save storage space and loading time.


## Contact Page
There is a form on the contact page that when filled will store a message in the database and assign a reference number. The admins will get a notification while the customer gets a submission confirmation.


## Customer Support Page
There is a form on the customer support page that when filled will store a support ticket in the database and assign a reference number. The admins will get a notification while the customer gets a submission confirmation.


## Cookie Policy detector
On the cookie policy page, I have implented jQuery that detects what cookies are being used and displays them on the page.


# Tests
Manual testing was performed on CRUD actions.
## Authentication
- Login (Completed)
- Sign Up (Completed)
- Forgot Password (Not Completed)


# Bugs
## Product Filtering and Sorting and Search
- BUG: Problem to filter by both brand and sort by price (Fixed)
- BUG: Cannot sort by price on a search result
## AllAuth - python manage.py runserver
- BUG: WARNINGS: account.EmailAddress: (models.W036) MySQL does not support unique constraints with conditions.

# Robots file
The robots file will block indexing of session specific URLS like a users Profile and orders, the basket, and the erp system.


# Sitemap
- [Django Sitemaps](https://docs.djangoproject.com/en/5.0/ref/contrib/sitemaps/)

...

# Deployment


## Collectstatic
Collectstatic is performed when DEBUG is False in order to sync files to AWS S3.
```
python manage.py collectstatic
```
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
- [Resize Images - Pillow](https://stackoverflow.com/questions/7970637/how-to-resize-the-new-uploaded-images-using-pil-before-saving)
- [Resize Images - Pillow](https://forum.djangoproject.com/t/django-filefield-resize-image-before-save-to-s3botostorage/7595)

## Product Images
- [TE0123456789](https://www.jumia.com.ng/generic-mini-digital-multimeter-voltmeter-voltage-ampere-tester-160778516.html)
- [3456789012](https://naughtonfarmmachinery.ie/products/swampmaster-stormgear-waterproof-jacket)
- [0123456789](https://www.thegreekfoundation.com/shop/home/espresso-cup)
- [Home page toolbox](https://media-www.canadiantire.ca/product/fixing/tools/tool-storage/0581370/maximum-57-8-drawer-chest-e21df9ca-ea32-43ad-b589-e86d1307c0c3-jpgrendition.jpg?impolicy=mZoom)