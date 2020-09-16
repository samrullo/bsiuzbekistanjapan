# Flask-SQLAlchemy with Microsoft SQL server

To connect to Microsoft SQL server with flask SQLAlchemy
we need to install ```pyodbc``` library.

SQLALCHEMY_DATABASE_URI will look like below
```python
mssql+pyodbc://<username>:<password>@<hostname>:<port>/<databasename>?driver=<driver to be used>
```

On Mac OS I needed to install ```unixodbc``` and other mssql odbc libraries.

To prevent permission errors to /usr/local directories
as per <a href="https://qiita.com/ArcCosine@github/items/2b8417fb3a0759045edb">this qiita link</a>
```python
sudo chown -R $(whoami) $(brew --prefix)/*
```

As per <a href="https://stackoverflow.com/questions/54302793/dyld-library-not-loaded-usr-local-opt-unixodbc-lib-libodbc-2-dylib">this stackoverflow link</a>
```python
brew install unixodbc

brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql mssql-tools
```