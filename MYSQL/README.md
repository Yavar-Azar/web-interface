# MYSQL





## Install 



install mysql and mariadb then we need some commands

```bash
mysql_secure_installation
sudo systemctl start mariadb.service
sudo systemctl stop mariadb.service

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

Now I have a database access and easy mysql command without pass

:warning: by defauly mysql creates db files in /var/lib/mysql path and it is better to change path or permission for example by

```bash
chmod -R 777 /var/lib/mysql
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

