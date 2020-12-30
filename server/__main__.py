from argparse import ArgumentParser
from daemon import DaemonContext  # type: ignore
from . import server


ap = ArgumentParser()
ap.add_argument('--daemonize', '-d', action='store_true', dest='daemonize')
args = ap.parse_args()

if args.daemonize:
    print('running server in background')
    with DaemonContext():
        server.run()
else:
    server.run()
