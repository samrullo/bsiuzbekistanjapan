# Install

```python
sudo apt update
```

```python
sudo apt install mysql-server
```

# Configuring mysql

```python
sudo mysql_secure_installation
```

This will take you through a series of prompts where you can make some changes to your MySQL installation’s security options. The first prompt will ask whether you’d like to set up the Validate Password Plugin, which can be used to test the strength of your MySQL password. Regardless of your choice, the next prompt will be to set a password for the MySQL root user. Enter and then confirm a secure password of your choice.

From there, you can press Y and then ENTER to accept the defaults for all the subsequent questions. This will remove some anonymous users and the test database, disable remote root logins, and load these new rules so that MySQL immediately respects the changes you have made.

To initialize the MySQL data directory, you would use mysql_install_db for versions before 5.7.6, and mysqld --initialize for 5.7.6 and later. However, if you installed MySQL from the Debian distribution, as described in Step 1, the data directory was initialized automatically; you don’t have to do anything. If you try running the command anyway, you’ll see the following error:

#Adjusting User Authentication and Privileges
n Ubuntu systems running MySQL 5.7 (and later versions), the root MySQL user is set to authenticate using the auth_socket plugin by default rather than with a password. This allows for some greater security and usability in many cases, but it can also complicate things when you need to allow an external program (e.g., phpMyAdmin) to access the user.

In order to use a password to connect to MySQL as root, you will need to switch its authentication method from auth_socket to mysql_native_password. To do this, open up the MySQL prompt from your terminal:

```python
sudo mysql
```

```python
mysql> SELECT user,authentication_string,plugin,host FROM mysql.user;
```

```python
Output
+------------------+-------------------------------------------+-----------------------+-----------+
| user             | authentication_string                     | plugin                | host      |
+------------------+-------------------------------------------+-----------------------+-----------+
| root             |                                           | auth_socket           | localhost |
| mysql.session    | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| mysql.sys        | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| debian-sys-maint | *CC744277A401A7D25BE1CA89AFF17BF607F876FF | mysql_native_password | localhost |
+------------------+-------------------------------------------+-----------------------+-----------+
4 rows in set (0.00 sec)
```

In this example, you can see that the root user does in fact authenticate using the auth_socket plugin. To configure the root account to authenticate with a password, run the following ALTER USER command. Be sure to change password to a strong password of your choosing, and note that this command will change the root password you set in Step 2:

```python
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

```python
mysql> FLUSH PRIVILEGES;
```

Next create a new user

```python
mysql> CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';
```

```python
mysql> GRANT ALL PRIVILEGES ON *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
```