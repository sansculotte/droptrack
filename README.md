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


API v2
------

for development

`export API_URL=http://127.0.0.1:5000`

for deploy

`export API_URL=https://soup.jetpack.cl/droptrack`

uploading file with curl

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" -F "soundfile=@\"./mp3/trk009-3.mp3\"" http://127.0.0.1:5000/files`

downloading file with curl

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" http://127.0.0.1:5000/files/trk013-4.mp3`

calling GET /autoedit to get help on the command in the JSON return

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/api/smp/autoedit`

calling POST autoedit with single file input with

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" -H "Content-Type: application/json" -X POST --data '{"filenames": ["trk013-4.mp3"]}' http://127.0.0.1:5000/api/smp/autoedit`


downloading result file with curl

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" http://127.0.0.1:5000/files/data/trk013-4-autoedit-0.wav`


calling GET /autocover to get help on the command in the JSON return

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/api/smp/autocover`

calling POST /autocover with a single file input and optional `"autocover_mode": {"feature_matrix", "recurrence_matrix"}` selector

`curl -H "X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7" -H "Content-Type: application/json" -X POST --data '{"filenames": ["trk013-4.mp3"]}' http://127.0.0.1:5000/api/smp/autocover`
