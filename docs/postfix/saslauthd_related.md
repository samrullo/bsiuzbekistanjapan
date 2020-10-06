# saslauthd

## to check saslauthd daemon is running
```python
sudo service --status-all | grep saslauthd
```

## to test sasl authentication
```python
testsaslauthd -u samrullo -r uzjapa.com -p 18Rirezu  -f /var/spool/postfix/var/run/saslauthd/mux -s smtp
```

I get below error
```python
connect() : No such file or directory
```

From
```python
smtpd_sasl_path = private/auth
```

to
```python
smtpd_sasl_path = smtpd
```

# solution to sasl authentication

I was struggling for days to get saslauthd authenticate with my system credentials

On cyrus documentation it said if we start ```saslauthd``` as below it will use system credentials
```python
saslauthd -a shadow
```

But above was giving me error saying can't make a directory
So I manually created that directory
```python
samrullo@mail:~$ sudo mkdir -p /var/state/saslauthd
```

Only after that below worked
```python
samrullo@mail:~$ testsaslauthd -u <username> -p <password>
```