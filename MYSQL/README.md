# MYSQL





## Install 

follow instruction in this link carrefully
https://forum.manjaro.org/t/howto-install-apache-mariadb-mysql-php-lamp/13000

install mysql and mariadb then we need some commands

In the Manjaro (archlinux)

```bash

sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

mysql_secure_installation
sudo systemctl start mariadb.service
sudo systemctl stop mariadb.service

```

Launch at reboot

```bash
sudo systemctl enable mysql
```


you must login root without sudo after this


if there is any problem and you need sudo go throw below steps


```bash

$ sudo mysql -u root # I had to use "sudo" since is new installation

mysql> USE mysql;
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
mysql> FLUSH PRIVILEGES;
mysql> exit;

$ sudo service mysql restart
```

## Mysql

Fisrt of all I need a user with **grant** anythinh without password

Create a user with current username:

```bash
sudo mysql -e "CREATE USER $USER"    
```

then i need to give all access to this user create database...

```sql
GRANT ALL PRIVILEGES ON * . * TO 'yavar'@'%';
flush privileges;
```

and then restart sql service

```bash
sudo systemctl start mariadb.service
sudo systemctl stop mariadb.service
```
for ubuntu check below lib 
```bash
sudo apt install libmysqlclient-dev
```



### Flask and mysql link

add these lines to your *app.py* to set database

```python
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'yavar'
#app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


```

## Create a table in mysql

- First we create a user table

```sql
CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), username VARCHAR(40), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```

- Also we need other database tables such as article

  ```sql
  CREATE TABLE articles(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), title VARCHAR(255), author VARCHAR(100), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
  ```

  
