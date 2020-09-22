# Letsencrypt
https://devanswers.co/lets-encrypt-ssl-apache-ubuntu-18-04/

At the end of the instructions when running
```python
sudo certbot --apache2
```
it throws error that trying to override existing WSGIProcess.

The solutions was provided in https://stackoverflow.com/questions/47803081/certbot-apache-error-name-duplicates-previous-wsgi-daemon-definition
According to it, we need to define VirtualHost with port 80 and 443 in the same file.
```python
WSGIApplicationGroup %{GLOBAL}
WSGIDaemonProcess myprocess user=ubuntu group=ubuntu threads=10 home=/home/ubuntu/myapp
WSGIProcessGroup myprocess

<VirtualHost *:80>
    ServerName example.com
    ...
</VirtualHost>
<VirtualHost *:443>
    ServerName example.com
    ...
</VirtualHost>WSGIApplicationGroup %{GLOBAL}
WSGIDaemonProcess myprocess user=ubuntu group=ubuntu threads=10 home=/home/ubuntu/myapp
WSGIProcessGroup myprocess

<VirtualHost *:80>
    ServerName example.com
    ...
</VirtualHost>
<VirtualHost *:443>
    ServerName example.com
    ...
</VirtualHost>
```

# important notes
IMPORTANT NOTES:
 - We were unable to install your certificate, however, we
   successfully restored your server to its prior configuration.
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/bsiuzbekistanjapan.southeastasia.cloudapp.azure.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/bsiuzbekistanjapan.southeastasia.cloudapp.azure.com/privkey.pem
   Your cert will expire on 2020-12-19. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"