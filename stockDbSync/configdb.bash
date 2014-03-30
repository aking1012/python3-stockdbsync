#!/bin/bash

#initial database connection
source ./dbsettings.bash

sudo su postgres -c "createuser -DIRSw $DB_USER"
sudo su postgres -c "psql -c \"ALTER USER $DB_USER PASSWORD '$DB_PASS'\""
sudo su postgres -c "psql -c \"DROP DATABASE $DB_USER\""
sudo su postgres -c "createdb $DB_USER -O $DB_USER"
