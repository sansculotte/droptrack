autoedit api 2 &lt;2021-01-03 So&gt;
------------------------------------

RES always includes {'status': http<sub>responsecode</sub>, 'message': human-readable}

### /app\[/session\]

-   POST {}
-   RES {'authtoken': 'ABCDEF1234'}

authtoken is then put into the http header of future client requests?

### /app/files

-   GET {'path': pathspec}, pathspec '', '/', ...
-   RES {'files': \[{'path': 'files/file1.bla', ...}, {'path': 'files/file2.blub'}, ...\]}

-   POST {'path': 'files/new/file.wav', 'data': 'binary/encoded'}
-   RES {'files': \[{'path': 'files/new/file.wav', 'size': size-in-bytes-on-server}\]}

-   PUT {'path': 'files/new/file.wav', 'data': 'binary/encoded'}
-   RES {'files': \[{'path': 'files/new/file.wav', 'size': size-in-bytes-on-server}\]}

-   DELETE {'path': 'files/new/file.wav'}
-   RES {'files': \[\]}

GET /app/files/file.bla {} = GET /app/files {'path': 'file.bla'}

If data is a URI fetch that from server or separate command?

merges droptrack and autowww funcs?

### /app/funcs

-   GET {}
-   RES {'funcs': \[{autoedit}, {...}\]}

### /app/funcs/autoedit

-   GET {}
-   RES {help}

-   POST {'arg1': arg1, 'arg2': arg2, ...}
-   RES {'files': \[{'path': 'file1-autoedit.wav'}, {'path': 'file1-autoedit.txt'}, {'path': 'file1-autoedit.pkl'}\], ...}

### /app/funcs/autoother

-   GET {}
-   RES {help}

-   POST {'arg1': arg1, 'arg2': arg2, ...}
-   RES {'files': \[{'path': 'file1-autoedit.wav'}, {'path': 'file1-autoedit.txt'}, {'path': 'file1-autoedit.pkl'}\], ...}


