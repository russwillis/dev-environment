# dev-environment
local version of a development environment

Steps to follow:

git clone this repository
usual vagrant up, vagrant ssh

# taken from https://www.digitalocean.com/community/tutorials/how-to-create-remove-manage-tables-in-postgresql-on-a-cloud-server

After installation, create a new user to manage the database we'll be creating:

```
sudo adduser postgres_user
```
Log into the default PostgreSQL user (called "postgres") to create a database and assign it to the new user:

```
sudo su - postgres
psql
```
You will be dropped into the PostgreSQL command prompt.

Create a new user that matches the system user you created. Then create a database managed by that user:

```
CREATE USER postgres_user WITH PASSWORD 'password';
CREATE DATABASE my_postgres_db OWNER postgres_user;
```

Exit out of the interface with the following command:

```
\q
```
Exit out of the default "postgres" user account and log into the user you created with the following commands:

```
exit
sudo su - postgres_user
```
Sign into the database you created with the following command:

```
psql my_postgres_db
```

# create the table by copying and pasting this into the console
```
CREATE TABLE public_address (
  address_id serial PRIMARY KEY,
  uprn varchar(25) NOT NULL,
  title_no varchar(10),
  saon varchar(50),
  paon varchar(50),
  street varchar(50),
  town varchar(50),
  county varchar(50),
  postcode varchar(9)
  );
```
