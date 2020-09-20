# to install apache2 on ubuntu

```
sudo apt-get update
sudo apt-get install apache2
```

Then I hadd to add inbound and outbound rules to allow connections
to port 80 from any source to any destination to my azure 
VM to allow http connection

Next to run python flask we need to install mod_wsgi
Refer to https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/
on instructions. ```mod_wsgi``` allows apache to serve python flask.

Be careful to install mod_wsgi module compatible with python3 as per https://stackoverflow.com/questions/37629929/apache2-using-python2-7-i-want-to-use-python3-4
```python
sudo apt-get install libapache2-mod-wsgi-py3
```

# mssql-tools on ubuntu
follow instructions on https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools?view=sql-server-ver15#ubuntu

You need to add the vm's IP to firewall rules of mssql

Then you can test your connection with 
```python
nc -zv bsiuzbekistanjapan.database.windows.net 1433
```

# mysql client
The easiest way is to install mysql-server on ubuntu
```python
sudo apt install mysql-server
```

Then 

```python
sudo apt-get install libmysqlclient-dev
```

Had to add below
```python
[mysqld]
skip-grant-tables
```

After installing mysql-server, couldn't login as usual user
To prevent that had to make changes to config file
```python
sudo vi /etc/mysql/my.cnf
```

# Some challenges faced when installing flask project on ubuntu 18.04
To check ubuntu version

```python
lsb_release -a
```

By default ```root``` user is the owner of ```/var/www``` directory.
To change the owner to current user
```python
sudo chown -R $USER:$USER /var/www
```

Azure vm didn't have pip installed by default. To install it
```python
sudo apt install python3-pip
```

Then to upgrade pip
```python
python3 -m pip install --user --upgrade pip
```

To be able to create virtualenv on ubuntu, I had to install
```python
sudo apt-get install python3-venv
```

Then from within the python project directory, I ran
```python
python3 -m venv venv
```

When installing python venv, I got error when install ```pyOpenSSL```
According to https://github.com/geerlingguy/JJG-Ansible-Windows/issues/28 I had to install
```python
libffi-dev + libssl-dev on Debian/Ubuntu, libffi-devel + something for openssl dev package on
```

When I wanted to upgrade to python3.7 I was getting error.
Then ran below. Apparently I needed to register extra repositories.
```python
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa 
sudo apt-get update
sudo apt-get install python3.6
```

To install alternative python3 versions
```python
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 3
sudo update-alternatives --config python3
```


After changing python3 alternative to newly installed python3.6
I was getting errors with creating virtualenv.
Based on https://stackoverflow.com/questions/53070868/how-to-install-python3-7-and-create-a-virtualenv-with-pip-on-ubuntu-18-04
```python
% sudo apt install python3.7 python3-venv python3.7-venv
% python3.7 -m venv py37-venv
% . py37-venv/bin/activate
(py37-venv) % 
```