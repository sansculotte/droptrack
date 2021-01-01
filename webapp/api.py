"""droptrack.webapp.api

The main mechanics of the webapp.

This is NOT proper REST.
"""


import os
from flask import (
    current_app,
    jsonify,
    request,
    url_for,
    session,
    send_from_directory,
    Blueprint,
    Response,
)
from werkzeug.utils import secure_filename
from .lib import (
    validate_url,
    validate_soundfile,
)

from multiprocessing import Process

from .smp_audio_tasks import run_autoedit_2

api = Blueprint('api', __name__)


def api_response_ok(data: dict) -> Response:
    data.update({'status': 'ok'})
    return jsonify(data)


def api_response_started(data: dict) -> Response:
    data.update({'status': 202})
    return jsonify(data)


def api_response_error(data: dict) -> Response:
    data.update({'status': 'error'})
    return jsonify(data)

############################################################
# routes: api extensional version
# exists: url, upload, download
#
# for autosuite
# func(name, arg1, ..., argn)
#   all args are refs
#   funcrefs: item, group, 
#   argrefs: item ref, group ref
#
#   funcs, items, groups can be listed
"""
enter: got root itemref, the dt_session 'abcd'
func('get', itemref)
returns: list of itemrefs


"""

@api.route('/autoedit', methods=['GET', 'POST'])
def autoedit() -> Response:
    """autoedit

    dummy function testing async
    """
    dt_item = 'None'
    if request.method == 'POST':
        request_data = request.form
        # request_data = request.files
    elif request.method == 'GET':
        request_data = request.args

    # current_app.logger.info(f'request.files {request.files}')
    current_app.logger.info(f'request.form {request.form}')
        
    if 'dt_item' in request_data:
        dt_item = request_data['dt_item']
    elif 'dt_item' not in request_data and 'dt_session' in request_data:
        dt_item = request_data['dt_session']
    elif 'dt_item[]' in request_data:
        dt_item = request_data.getlist('dt_item[]')
        # current_app.logger.info(f'dt_item {len(dt_item)}')
        # for dt_item_i in request_data['dt_item[]']:
        #     current_app.logger.info(f'dt_item_i {dt_item_i}')
        #     dt_item = [_ for _ in request_data['dt_item[]']]
        
    current_app.logger.info(f'dt_item type {type(dt_item)} data {dt_item}')

    # # do the work and get the item
    # if dt_item in current_app.dt_data:
    #     dt_item_path = current_app.dt_data[dt_item]['path']
    #     current_app.logger.info(f'item dt_item[path] {dt_item_path}')

    # do the work and get the item
    # if dt_item_dict in current_app.dt_data_list:
    
    if type(dt_item) in [list]:
        dt_item_dict = []
        for dt_item_ in dt_item:
            dt_item_dict += [_ for _ in current_app.dt_data_list if _['dt_item'] == dt_item_]
    else:
        dt_item_dict = [_ for _ in current_app.dt_data_list if _['dt_item'] == dt_item]
    dt_item_path = []
    # if len(dt_item_dict) > 0:
    for dt_item_dict_i in dt_item_dict:
        dt_item_path.append(dt_item_dict_i['dt_item_path'])
        
    current_app.logger.info(f'item dt_item_path {dt_item_path}')

    # get function parameters / defaults
    # for dt_params in ['dt_verbose', 'dt_assemble_mode', 'dt_duration',
    #                   'dt_numsegs', 'dt_seed']:
    
    dt_assemble_mode = 'random'
    dt_numsegs = 60
    dt_duration = 45
    dt_seed = 1234
    dt_verbose = False
    
    if 'dt_assemble_mode' in request_data:
        dt_assemble_mode = request_data['dt_assemble_mode']
    if 'dt_numsegs' in request_data:
        dt_numsegs = request_data['dt_numsegs']
    if 'dt_duration' in request_data:
        dt_duration = request_data['dt_duration']
    if 'dt_seed' in request_data:
        dt_seed = request_data['dt_seed']
    if 'dt_verbose' in request_data:
        dt_verbose = request_data['dt_verbose']

    # Create a daemonic process with heavy "my_func"
    heavy_process = Process(  
        # target=my_func,
        target=run_autoedit_2,
        kwargs={
            'filenames': dt_item_path,
            'assemble_mode': dt_assemble_mode,
            'numsegs': dt_numsegs,
            'duration': dt_duration,
            'seed': dt_seed,
            'verbose': dt_verbose,
            'rootdir': 'data/dt_sessions/zniz'
        },
        daemon=True,
    )
    heavy_process.start()
    return api_response_started({
        'message': 'autoedit started',
    })

# async testing, define some heavy function
def my_func(**kwargs):
    import time
    current_app.logger.info(f"my_func Process start with {kwargs}")
    time.sleep(3)
    current_app.logger.info("my_func Process finished")

    
@api.route('/item', methods=['GET', 'POST'])
def item() -> Response:
    """
    Accept soundfile url
    """
    dt_item = 'None'
    if request.method == 'POST':
        request_data = request.form
        # current_app.logger.info(f'item request.form {list(request.form.keys())}')

        # if 'dt_item' in request.form:
        #     dt_item = request.form['dt_item']
        # elif 'dt_item' not in request.form and 'dt_session' in request.form:
        #     dt_item = request.form['dt_session']
    elif request.method == 'GET':
        request_data = request.args
        # current_app.logger.info(f'item request.form {list(request.form.keys())}')

        # if 'dt_item' in request.args:
        #     dt_item = request.args['dt_item']
        # elif 'dt_item' not in request.args and 'dt_session' in request.args:
        #     dt_item = request.args['dt_session']

    if 'dt_item' in request_data:
        dt_item = request_data['dt_item']
    elif 'dt_item' not in request_data and 'dt_session' in request_data:
        dt_item = request_data['dt_session']

    #     url = request.json.get('url')
    #     if validate_url(url):
    #         current_app.queue.send(url)
    #         return api_response_ok({'message': 'Url accepted'})
    #     else:
    #         return api_response_error({'message': 'Invalid url'})
    # return Response(status=405)

    current_app.logger.info(f'item requested dt_item {dt_item}')

    # # do the work and get the item
    # if dt_item in current_app.dt_data:
    #     dt_item_path = current_app.dt_data[dt_item]['path']
    #     current_app.logger.info(f'item dt_item[path] {dt_item_path}')
    # else:
    #     dt_item_path = "None"
        
    # do the work and get the item
    # if dt_item in current_app.dt_data:
    dt_item_dict = [_ for _ in current_app.dt_data_list if _['dt_item'] == dt_item]
    if len(dt_item_dict) > 0:
        # dt_item_path = current_app.dt_data[dt_item]['path']
        dt_item_path = dt_item_dict[-1]['dt_item_path']
        current_app.logger.info(f'item dt_item[path] {dt_item_path}')
    else:
        dt_item_path = "None"
        
    # item content
    if os.path.isdir(dt_item_path):
        # dt_item_content = dict([(dt_item + "_" + _, os.path.join(dt_item_path, _)) for _ in os.listdir(dt_item_path)])
        dt_item_content = [{
            'dt_item': os.path.join(dt_item, _),
            'dt_item_path': os.path.join(dt_item_path, _)} for _ in os.listdir(dt_item_path)]
    elif os.path.isfile(dt_item_path):
        # dt_item_copy = [_ for _ in current_app.dt_data if _ == dt_item][0]
        dt_item_copy = dt_item_dict[-1]['dt_item']
        dt_item_content = [{
            'size': os.path.getsize(dt_item_path),
            # 'dt_item': dt_item,
            'dt_item_copy': dt_item_copy,
        }]
        # dt_item_content = [os.path.join(dt_item_path, _) for _ in  os.listdir(dt_item_path)]
    else:
        dt_item_content = []
    
    return api_response_ok({
        'message': 'item OK',
        'dt_item': dt_item,
        'dt_item_content': dt_item_content,
    })


@api.route('/url', methods=['POST'])
def url() -> Response:
    """
    Accept soundfile url
    """
    # TODO: requires server/player to be up to do the actual download
    if request.method == 'POST':
        url = request.json.get('url')
        if validate_url(url):
            current_app.queue.send(url)
            return api_response_ok({'message': 'Url accepted'})
        else:
            return api_response_error({'message': 'Invalid url'})
    return Response(status=405)

@api.route('/upload', methods=['POST'])
def upload() -> Response:
    """
    Accept direct soundfile upload per multipart/form-data
    """
    if request.method == 'POST':
        soundfile = request.files.get('soundfile')

        # current_app.logger.info([_ for _ in request.form.keys()])
        
        # dt_session check
        # if 'dt_session_dir_path_uploaded' in request.form:
        if 'dt_session' in request.form:
            upload_dir = os.path.join(
                current_app.config['DATA_DIR'],
                'dt_sessions',
                request.form['dt_session'],
                'uploaded'
            )
        elif 'dt_session_dir_path_uploaded' in session:
            upload_dir = session['dt_session_dir_path_uploaded']
        else:
            upload_dir = current_app.config['UPLOAD_DIR']

        # log
        current_app.logger.info(f'upload {upload_dir} type(soundfile) {type(soundfile)}')
        current_app.logger.info(f'request content length {request.content_length}')
            
        if soundfile and validate_soundfile(soundfile):
            filename = secure_filename(soundfile.filename)
            location = os.path.join(
                upload_dir,
                filename
            )
            soundfile.save(location)
            soundfilesize = os.path.getsize(location)
            
            # trigger player for redownload
            url = url_for('api.download', filename=filename, _external=True)
            current_app.queue.send(url)

            # return response
            return api_response_ok({
                'message': 'File accepted',
                'soundfilesize': soundfilesize,
            })
        else:
            return api_response_error({'message': 'Invalid File'})
    return Response(status=405)

@api.route('/download/<string:filename>')
def download(filename: str) -> Response:
    return send_from_directory(
        current_app.config['UPLOAD_DIR'],
        filename,
        as_attachment=True
    )
