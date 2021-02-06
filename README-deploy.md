# How to deploy droptrack from an smp_audio perspective

There are a few related approaches to handle provisioning and
deployment. The upstream approach is in `deploy/deploy.sh` and needs
documentation. There is also an `ansible` playbook which I haven't
fully figured out yet.

## owald journey initial

First time round need to set up / fix a few things. Provisioning
light.

Create a 'deploy' user on the remote system which we will use to log
in to the server, set up and update stuff, and to restart the app when
the update is done.

When the user is created, copy your SSH key to that user's
authorized_keys file with

`ssh-copy-id deploy@deployhost`

Once logged in the initial interactive setup session goes like this:

```bash
cd /path/to/webroot
git clone https://github.com/x75/droptrack.git
cd droptrack
virtualenv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/pip install -r smp-audio-requirements.txt
./venv/bin/flask db stamp
./venv/bin/flask db upgrade
# migrating real data, sql file has been prepared beforehand
cat /path/to/dev/droptrack/droptrack.sql | sqlite3 droptrack.db
npm install
npm run build
# copy data
cd /path/to/dev/droptrack/data/upload
for name in `sqlite3 ../../droptrack.db "select name from User;"` ; do rsync -av --progress $name /home/www/droptrack-x75/data/upload/ ; done
# test new server with flask/uwsgi manual
./run_webapp.sh
uwsgi --uwsgi-socket 0.0.0.0:3031 --callable app -w app --master --processes 1 --threads 1
# change uwsgi droptrack.ini to new directory
sudo service uwsgi restart
```

If there is any trouble with

`RuntimeError: cannot cache function '__shear_dense'`

this is a permission problem. Do a

`chown -R deploy.deploy /path/to/webroot/droptrack`

There also was an issue with getting the SQLALCHEMY_DATABASE_URI from
the env, hardcoded that for now into the production config.

## owald journey quick deploy

When that is done once, quick deploy is done by this
```bash
ssh deploy@deployhost <<ENDSSH
cd /home/www/droptrack-x75
git checkout -f
git pull
npm install
npm run build
sudo service uwsgi restart
ENDSSH
```

## notes

create 'deploy' user on remote system

copy deploy/inventory.dist to deploy/inventory

ansible-playbook deploy/playbook.yml

ansible-playbook -i deploy/inventory deploy/playbook.yml
