# WuliuGo Project

This project is dedicated to building a Web service of Go AI. It use KataGo as the analysis engine and Flask as backend service.

+ User Management
+ Game Management
+ GPU Management



# How to use?

+ crete database

```
docker pull mariadb
docker run --name mariadb_go -p 3307:3306 -e MYSQL_ROOT_PASSWORD=mrwuliu -v <select a path to save>:/var/lib/mysql -d mariadb
```

+ set config

```
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>:<password>@<ip>:<port>/<database>'
SECRET_KEY  = '<your secret key>'
```

if you use the docker command, you can set this example config:

```
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mrwuliu@localhost:3307/go'
SECRET_KEY  = 'BIGBIGBIGBIGBIGDDDIAMWulLuiiuGGo12GO2'
```

+ set environment

before use, you need install Python3.12+

```
pip install virtualenv
```

```
cd ~/WuliuGo
pip install -r requirement.txt
```

+ run

```
flask run
```







