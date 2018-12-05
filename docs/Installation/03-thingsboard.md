# ThingsBoard installation

The Thingsboard IoT platform (<https://thingsboard.io>) has been installed on a Debian 9 Linux OS.

The following installation steps are based on documentation: <https://thingsboard.io/docs/user-guide/install/linux/>

## External database installation

We chose to use postgreSQL which seems to require less memory than Cassandra the other database supported by ThingsBoard.

For installing and running postgreSQL:

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
    sudo service postgresql start

Create user and database for thingsboard:

    $ sudo -u postgres createuser --interactive
    Saisir le nom du rôle à ajouter : thingsboard
    Le nouveau rôle est-il super-utilisateur ? (o/n) n
    Le nouveau rôle est-il autorisé à créer des bases de données ? (o/n) n
    Le nouveau rôle est-il autorisé à créer de nouveaux rôles ? (o/n) n
    $ sudo -u postgres createdb thingsboard

Add a password for user thingsboard (<https://blog.2ndquadrant.com/how-to-safely-change-the-postgres-user-password-via-psql/>):

    $ sudo -u thingsboard psql
    thingsboard=> \password
    Saisissez le nouveau mot de passe :
    Saisissez-le à nouveau :
    thingsboard=> \q

Grant privileges for the user thingsboard (<https://stackoverflow.com/a/22486012>):

    $ sudo -u postgres psql
    postgres=# GRANT CONNECT ON DATABASE thingsboard TO thingsboard;
    GRANT
    postgres=# GRANT USAGE ON SCHEMA public TO thingsboard;
    GRANT
    postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO thingsboard;
    GRANT
    postgres=# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO thingsboard;
    GRANT
    postgres=# \q

## Installation of thingsBoard

Search the link for the last version of thingsboard here: <https://github.com/thingsboard/thingsboard/releases>

Installation steps with version 2.2:

    cd /tmp
    wget https://github.com/thingsboard/thingsboard/releases/download/v2.2/thingsboard-2.2.deb
    sudo dpkg -i thingsboard-2.2.deb
    sudo /usr/share/thingsboard/bin/install/install.sh

Edit configuration file:

    sudo nano /etc/thingsboard/conf/thingsboard.yml

Follow instructions at <https://thingsboard.io/docs/user-guide/install/linux/>.
On our server, the port has been modified from 8080 to 8082 (8080 and 8081 are already used by other servers).

Then start service:

    sudo service thingsboard start

## Installation de pgAdmin (aborted)

Follow instructions here: <https://wiki.postgresql.org/wiki/Apt>

For installation in server mode (<https://www.pgadmin.org/docs/pgadmin4/3.x/server_deployment.html>):

    sudo mkdir /var/log/pgadmin
    sudo chown www-data:www-data /var/log/pgadmin
    sudo mkdir /var/lib/pgadmin
    sudo chown www-data:www-data /var/lib/pgadmin
    sudo apt-get install python-flask python-pip
    sudo python -m pip install flask-babelex
    sudo python -m pip install flask-login
    sudo python -m pip install flask-mail
    sudo python -m pip install flask-paranoid
    sudo python -m pip install flask-security
    sudo python -m pip install flask-sqlalchemy
    sudo python -m pip install dateutil
    sudo python -m pip install flask_migrate
    sudo apt-get install python-psycopg2

Aborted after missing dependency "backports" which I was enable to find. It seems that another way of installation is approved: <https://stackoverflow.com/a/41260478>



