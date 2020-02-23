from .server import Server


config = {
    'upload_dir': './data/upload',
    'sockets': {
        'webapp': 'tcp://127.0.0.1:5100',
        'player': 'tcp://127.0.0.1:5200'
    }
}


server = Server(config)
