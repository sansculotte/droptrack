Droptrack
=========

Bring your own track to the party


Requirements
------------

- python3.6+
- pip
- node
- npm
- curl
- moc
- zmq
- postgres
- smp_audio https://github.com/x75/smp_audio


Setup
-----

Setup your python environment, through virtualenv or your preferred method.

Install python dependencies

    pip install -r requirements
    pip install -r dev-requirements

Copy config.py.dist to config.py and tweak where nessecary.
Copy .env.dist to .env and tweak where nessecary.

Setup node environment, through your preferred method for the webapp frontend.

Install js dependencies

    npm install

Install postgres through your system's package manager or container, whatever your preferred method.
A Dockerfile is provided in etc/postgres

Run migrations

    flask db upgrade

Create User

    ./cli.py user create <name> <email>
    -> <password>
    -> <api_key>

*Webapp/Server*

    npm install
    npm run build
    ./run_webapp.sh
    ./run_server.sh

*Player*

    ./run_player.sh


Production Deploy
-----------------

Do not use the flask dev server in production, because reasons:
https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/#run-with-a-production-server
https://stackoverflow.com/questions/12269537/is-the-server-bundled-with-flask-safe-to-use-in-production

There is bash script for the production deploy of the webapp, which
should be doing the right things, assuming the following requirements are met:
- create a privileged deploy user on the target system
- install and configure postgres database
- install uwsgi

There is an [ansible playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) guiding you
through setting up the production environment. 
