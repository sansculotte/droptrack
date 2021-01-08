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


Setup
-----

Setup your python environment, through virtualenv or your preferred method.

Setup node environment, nvm or your preferred method.

Install python dependencies

    pip install -r requirements
    pip install -r dev-requirements

Install postgres

system install, container (your preferred method)

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
