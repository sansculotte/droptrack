## API v3 autoedit
### Setup

Configure your API_URL, for development like

`export API_URL=http://127.0.0.1:5000`

and for a production host

`export API_URL=https://soup.jetpack.cl/droptrack`

API calls are listed below and mapped to a curl command. Requests
require an authentication field in the header. To make the commands
below shorter, this is put into a command line fragment included in
the curl call. There are two types of requests required for the /files
and /smp parts of the namespace, each getting their own
fragment. Replace
`yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7`
with a valid key and create both fragments with

```echo -e "-H \"X-Authentication: yuOJX-8paOqRJR8iefr7vL-Ozu5owbSUtr8SIM0K1L1EKPB9mWjPM52nydMEFyl7\"" >headauth```

followed by

```echo `cat headauth` "-H \"Content-Type: application/json\"" >headjson```

### API file upload / download

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
