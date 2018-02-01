==================
Running the mysite 
==================
Assuming you use virtualenv, follow these steps to download and run the mysite in this directory:

::

    $ git clone git@github.com:yjb767868009/mysite.git
    $ virtualenv mysiteenv
    $ source mysiteenv/bin/activate
    $ cd mysite
    $ pip install -r requirement.txt
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ ln -s ~/path/to/your/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/
    $ python manage.py collectstatic
    $ /etc/init.d/nginx restart 


