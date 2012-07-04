TODO:
Post Formatting
     Allow HTML formatted text in posts.
     Adjust DB to reflected strings that are formatted
     Validate text, escape stuff if needed

Book Formatting
     Setup book layout to work properly
     Adjust text files to allow for more formatting options.
     Add Javascript to make book more interactive on single page

DB entry from site
     ALlow Admins to insert/edit/delete posts with user interface
     Allow all users to enter/edit Good bad ugly stuff
     	   File creation from form
     Allow users to insert/edit pictures
     
To Set up:

sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo pip install django
sudo pip install jinja2
sudo pip install django-photologue
sudo pip install docutils
sudo pip install sphinx	
sudo pip install django-tinymce
sudo apt-get install python-docutils
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
