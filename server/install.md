# Install MariaDB
`sudo apt install mariadb-server mariadb-backup libmariadb-dev`

# Run secure install
`sudo mysql_secure_installation`

# Set up database
`sudo mariadb` or `mariadb -u root -p`

## In MariaDB:
`CREATE DATABASE airpy DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;`

`GRANT ALL ON airpy.* TO 'airpy'@'localhost' IDENTIFIED BY 'airpy';`

`FLUSH PRIVILEGES;`

`EXIT;`