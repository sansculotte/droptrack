# How to deploy droptrack from an smp_audio perspective

There are a few related approaches to handle provisioning and
deployment. The upstream approach is in `deploy/deploy.sh` and needs
documentation. There is also an `ansible` playbook which I haven't
fully figured out yet.

## owald naive bottom-up approach

First time round need to set up / fix a few things. Provisioning, right?

Create a 'deploy' user on the remote system which we will use to log
in to the server, set up stuff, update stuff, restart the app when done.

When created copy your SSH key to that user's authorized_keys file.

Initial setup session once logged in goes like this:

cd /home/www

git clone https://github.com/x75/droptrack.git droptrack-x75

cd droptrack-x75

git checkout deploy-opt

virtualenv venv

./venv/bin/pip install -r requirements.txt

./venv/bin/pip install -r smp-audio-requirements.txt

./venv/bin/flask db stamp

./venv/bin/flask db upgrade

migrating real data

cat /home/x75/src/droptrack/droptrack.sql | sqlite3 droptrack.db

npm install

npm run build

chgrp -R www-data data/upload/

cd old-dev-dir

for name in `sqlite3 ../../droptrack.db "select name from User;"` ; do rsync -av --progress $name /home/www/droptrack-x75/data/upload/ ; done

test new server with flask/uwsgi manual

./run_webapp.sh

uwsgi --uwsgi-socket 0.0.0.0:3031 --callable app -w app --master --processes 2 --threads 2

change uwsgi droptrack.ini to new directory

restart uwsgi

if there is any trouble with

RuntimeError: cannot cache function '__shear_dense' 

just is a permission problem. dir right now is owned deploy.deploy

there also was an issue with getting the SQLALCHEMY_DATABASE_URI from the env, hardcoded that for now

## notes

create 'deploy' user on remote system

copy deploy/inventory.dist to deploy/inventory

ansible-playbook deploy/playbook.yml

ansible-playbook -i deploy/inventory deploy/playbook.yml
