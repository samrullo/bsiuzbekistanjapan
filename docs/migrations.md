# Database migrations

## Introduction
As you make progress developing an application, you will find
that your database models need to change, and when that
happens the database needs to be updated as well.
Flask-SQLAlchemy creates database tables only when they
do not exist already, so the only way to make it update
tables is by destroying the old tables first - but of course
this causes all the data in the database to be lost.

A better solution is to use a <i>database migration</i>
framework.

```
$pip install flask-migrate
``` 

```python
from flask_migrate import Migrate
...
migrate=Migrate(app,db)
```

Before creating tables ensure that you import Models in the file where you 
instantiate Migrate.
```python
from models import User, Product, SomeOtherModel
...
migrate=Migrate(app,db)
```

When you work on a new project, you can add support for database
migrations with the init subcommand
```
$flask db init
```
This command creates a migrations directory where all the migration
scripts will be stored.
<br>
In Alembic, a database migration is represented by a migration
script. This script has two functions called upgrade()
and downgrade(). The upgrade() function applies the database changes
that are part of the migration, and the downgrade() function
removes them.
<br>
To make changes to your database schema with Flask-Migrate, the following
procedure needs to be followed.
- Make necessary changes to model classes
- Create an automatic migration 
```python
$ flask db migrate
```
- Review the generated script and adjust it so that it
accurately represents the changes that were made to the models

- Add the migration script to the source code control
- Apply the migration
```python
$ flask db upgrade
``` 