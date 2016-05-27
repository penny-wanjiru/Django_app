# Django bucketlist app
  This bucketlist app consists of an Rest API and a frontend built with django templates. 

# Dependencies:
###Backend dependencies:
    Django - The backbone upon which this REST API is built upon. It's a Python web framework that features models, views, url routes and user management among many other features.

    Django REST framework - This is a powerful and flexible toolkit for building browsable REST APIs. It includes support for model serialization, permissions (default and custom) and viewsets among other features.

    Drf docs - This package is built on top of Django REST framework. It generates API documentation.
###Frontend dependencies:

    Materialize CSS - The front end framework from which all the elements and controls on the front end have been created.

    Sweet Alert - A beautiful replacement for Javascript's "Alert" dialog. Used when the user is required to confirm delete operations on the front end.

# Features:
*  A user can log in.
*  A user is authenticated.
*  Create new bucketlist.
*  Create new bucketlist items.
*  Update and delete the items.
*  Retrieve a list of all created bucket lists by a registered user.

## Usage:

* Clone the repo: git@github.com:andela-pwanjiru/Django_app.git

* Install requirements.
 `pip install -r requirements.txt`

* Install the project's database. PostgreSQL was used for this checkpoint.

* After installation, create a database on PostgreSQL for this app.

* Perform database migrations.
    `python manage.py makemigrations api`
    `python manage.py migrate api`

* Run the application
 `python manage.py runserver`


## API EndPoints
Access to all endpoints except login and registration require authentication.

To view this API's documentation, visit /docs while the app is running to view the resources.



## Testing
To run tests:
`python manage.py test`
