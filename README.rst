==========
README.TXT
==========

Prerequisites
-------------

Apache
Django
pip
docutils


Installation
------------

To Set up:
Run the following commands to install the dependencies and required programs.

::

sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo pip install django
sudo pip install jinja2
sudo pip install django-photologue
sudo pip install docutils
sudo pip install django-tinymce
sudo pip install PIL
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi


what files to copy / where
copy httpd.conf to /etc/apache2/
copy settings to husky_saxes
copy sax_settings to husky_saxes/src
copy saxes.db to husky_saxes

From husky_saxes/
chmod a+r . -R
chmod a+rw . saxes.db

Configuration
-------------

Running the webservice
----------------------

TODO
----

Post Formatting
     Validate text, escape stuff if needed

Book Formatting
     Setup book layout to work properly
     Adjust text files to allow for more formatting options.
     Add Javascript to make book more interactive on single page

DB entry from site
     Allow Admins to insert/edit/delete posts with user interface
	 Allow Admins to insert/edit members
     Allow all users to enter/edit Good bad ugly stuff
     	   File creation from form
     	   
     Allow users to insert/edit pictures
	 	 
DB schema
	Members
		Adjust field restrictions
		
		remove memory, add rank, username/password?, active
		
	Quotes
		Adjust field restrictions
			Longer Quote length
			
	Post
		Adjust field restrictions
			Longer Posts, add TinyMCE to body entry.
