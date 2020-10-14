# postfix tls

to enable tls we will have to open firewall to ports like 587, 465
```python
sudo ufw allow 80,443,587,465,143,993/tcp
```

And set configurations like below
```python
smtpd_tls_key_file = /etc/letsencrypt/live/uzjapa.com/privkey.pem
smtpd_tls_cert_file = /etc/letsencrypt/live/uzjapa.com/fullchain.pem
```
