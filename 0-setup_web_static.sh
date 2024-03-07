#!/usr/bin/env bash

# Update package lists and install nginx
apt-get -y update
apt-get -y install nginx

# Create necessary directories
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# Create index.html file with sample content
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link to current release
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of directories to ubuntu user
chown -R ubuntu:ubuntu /data/

# Add configuration for serving static files
sed -i "61i\
\tlocation /hbnb_static {\
\t\talias /data/web_static/current;\
\t\tautoindex off;\
\t}" /etc/nginx/sites-available/default

# Restart nginx service
service nginx restart
