# MySQL commands

To connect to mysql host

```
mysql -h localhost -u myname -p mydb
```

To create a user and give all privileges
```
mysql> CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
```

# macOs deal with can't connect via /tmp/mysql.sock

If you have MAMP, it already has its internal mysql server.
All you need is symlink /tmp/mysql.sock to /Applications/MAMP/tmp/mysql/mysql.sock

```
ln -s /Applications/MAMP/tmp/mysql/mysql.sock /tmp/mysql.sock
```