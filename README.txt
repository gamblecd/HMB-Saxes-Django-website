To Set up:

sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo pip install django
sudo pip install jinja2
sudo pip install django-photologue
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi

what files to copy / where
copy httpd.conf to /etc/apache2/
copy settings to husky_saxes
copy sax_settings to husky_saxes/src
copy saxes.db to husky_saxes

From husky_saxes/
chmod a+r . -R
chmod a+wx saxes.db
