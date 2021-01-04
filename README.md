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


Setup
-----

Setup your python environment, virtualenv or other method.

Setup node environment, nvm or other method.

Install python dependencies

    pip install -r requirements
    pip install -r dev-requirements


*Webapp/Server*

    npm install
    npm run build
    ./run_webapp.sh
    ./run_server.sh

*Player*

    ./run_player.sh


Deploy
------

Directory deploy has an ansible playbook and configuration templates to provision a
droptrack server.
https://docs.ansible.com/ansible/latest/user_guide/playbooks.html

Use fabric to deploy new iterations.
