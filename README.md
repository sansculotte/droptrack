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


API
---

uploading file with curl

`curl -v -F "soundfile=@\"./trk010-3.mp3\"" -F "dt_session=zniz"  http://127.0.0.1:5000/upload`

calling item with curl

`curl -v -X POST --data "dt_item=zniz_ul_trk011-3.mp3" http://127.0.0.1:5000/item`

calling download with dt_item

`curl -v -F "dt_item=zniz/uploaded/data/trk010-3-autoedit-5.wav" http://127.0.0.1:5000/download --output trk010-3-autoedit-5.wav`

calling autoedit from the command line with single file input

`curl -v -X POST --data "dt_item=zniz/uploaded/trk010-3.mp3" http://127.0.0.1:5000/autoedit`

calling autoedit from the command line with multiple file inputs

`curl -v -F "dt_item[]=zniz/uploaded/trk010-3.mp3" -F "dt_item[]=zniz/uploaded/trk011-3.mp3" http://127.0.0.1:5000/autoedit`

UNTESTED: calling autoedit with browser GET

<http://127.0.0.1:5000/autoedit?dt_item=zniz_ul_trk011-3.mp3>

