# Droptrack

Bring your own track to the party


## Requirements

- python3.6+
- pip
- node
- npm
- curl
- moc
- zmq


## Setup

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


## API v2

### Setup

Configure your API_URL, for development like

`export API_URL=http://127.0.0.1:5000`

and for deploy to your API host

`export API_URL=https://soup.jetpack.cl/droptrack`

All requests require an authentication and a content-type header. To
make the commands shorter it is good to put these redundant bits into
a curl command line fragment and include that in the call. First
create the fragment with

```echo -e "-H \"X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7\"" >headauth
echo -e "-H \"X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7\"\n-H \"Content-Type: application/json\"" >headjson
```

### API file upload / download

All API calls mapped to curl commands

Uploading a file via POST /files

`curl -K headauth -F "soundfile=@\"./mp3/trk009-3.mp3\"" ${API_URL}/files`

Download the directory tree via GET /files

`curl -K headauth ${API_URL}/files`

this returns the full directory tree from the top level and needs to be handled at the client.

Download a file via GET /files/path/to/filename.wav

`curl -K headauth ${API_URL}/files/path/to/filename.wav`

### API autoedit

GET /autoedit returns the autoedit help as JSON

`curl -K headjson -X GET ${API_URL}/api/smp/autoedit`

POST /autoedit with JSON configuration starts an autoedit process with
the given configuration and returns a process handle/queue location to
poll the status. Return an output filename directly?

`curl -K headjson -X POST --data '{"duration": 60, "filenames": ["trk013-4.mp3"]}' ${API_URL}/api/smp/autoedit`

Download the result file like above with GET /files/data/trk013-4-autoedit-0.wav

`curl -K headauth ${API_URL}/files/data/trk013-4-autoedit-0.wav`

### API autocover

calling GET /autocover to get help on the command in the JSON return

`curl -K headjson -X GET ${API_URL}/api/smp/autocover`

calling POST /autocover with a single file input and optional `"autocover_mode": {"feature_matrix", "recurrence_matrix"}` selector

`curl -K headjson -X POST --data '{"filenames": ["trk013-4.mp3"]}' ${API_URL}/api/smp/autocover`

### API automaster

GET /automaster returns the help on the automaster command as JSON

`curl -K headjson -X GET ${API_URL}/api/smp/automaster`

POST /automaster with JSON configuration

`curl -K headjson -X POST --data '{"filenames": ["trk013-4.mp3"], 'references': ['cooltrack.mp3']}' ${API_URL}/api/smp/automaster`

