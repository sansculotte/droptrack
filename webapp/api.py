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

from .filesys import walkdirlist

from multiprocessing import Process

from .smp_audio_tasks import ns2kw, kw2ns
from .smp_audio_tasks import run_autoedit_2, autoedit_conf_default

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
# api definition: all routes
# file in/out: url, upload, download
# file sys: item
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
    dt_item = None
    if request.method == 'POST':
        request_data = request.form
        # request_data = request.files
    elif request.method == 'GET':
        request_data = request.args

    # current_app.logger.info(f'api.autoedit request.files {request.files}')
    # current_app.logger.info(f'api.autoedit request.form {request.form}')
        
    if 'dt_item' in request_data:
        dt_item = request_data['dt_item']
    # elif 'dt_item' not in request_data and 'dt_session' in request_data:
    #     # FIXME: this doesnt work
    #     dt_item = request_data['dt_session']
    elif 'dt_item[]' in request_data:
        dt_item = request_data.getlist('dt_item[]')
        
    current_app.logger.info(f'api.autoedit dt_item type {type(dt_item)}')
    current_app.logger.info(f'api.autoedit dt_item data {dt_item}')

    # check params
    if dt_item is None:
        return api_response_error({
        'message': 'autoedit dt_item is None',
    })

    # convert single dt_item to list
    if type(dt_item) not in [list]:
        dt_item = [dt_item]

    # # create argument list by mapping requested dt_items to existing
    # # dt_items in dt_data_list
    # dt_item_dict = [_ for _ in current_app.dt_data_list if _['dt_item'] in dt_item]
    # current_app.logger.info(f'api.autoedit dt_item_dict {dt_item_dict}')

    # create argument list with file paths only
    # dt_item_path = [_['dt_item_path'] for _ in dt_item_dict]
    # # this is nice but destroys the order of the input arguments
    # dt_item_path = [_['dt_item_path'] for _ in current_app.dt_data_list if _['dt_item'] in dt_item]

    # create file paths only list from dt_item
    dt_item_path = []
    for dt_item_i in dt_item:
        dt_item_path += [_['dt_item_path'] for _ in current_app.dt_data_list if _['dt_item'] == dt_item_i]
    current_app.logger.info(f'api.autoedit dt_item_path {dt_item_path}')

    # configure and run autoedit
    autoedit_conf = kw2ns(autoedit_conf_default)
    # current_app.logger.info(f'api.autoedit autoedit_conf_default {autoedit_conf}')
    for k in autoedit_conf_default:
        k_req = f'dt_{k}'
        if k_req in request_data:
            v_req = request_data[k_req]
            setattr(autoedit_conf, k, v_req)
            
    # copy filename from request
    autoedit_conf.filenames = dt_item_path
    # autoedit_conf.rootdir = 'data/dt_sessions/zniz'
    autoedit_conf.rootdir = current_app.dt_session_data_dir
    
    current_app.logger.info(f'api.autoedit autoedit_conf {autoedit_conf}')

    # Create a process with "heavy" computation, anything taking more
    # than a few seconds
    heavy_process = Process(  
        target=run_autoedit_2, # my_func
        # args=autoedit_conf,
        kwargs={
            'autoedit_conf': autoedit_conf,
            # 'filenames': dt_item_path,
            # 'rootdir': 'data/dt_sessions/zniz'
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
    # default dt_item
    dt_item = 'default'
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

    current_app.logger.info(f'api.item requested dt_item {dt_item}')

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

            # update app.dt_data
            current_app.dt_data_list = walkdirlist(
                startpath=current_app.dt_sessions_dir,
                absroot=current_app.config.get('DATA_DIR'),
            )

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

@api.route('/download', methods=['GET', 'POST'])
def download_dt_item() -> Response:
    if request.method == 'POST':
        request_data = request.form
    elif request.method == 'GET':
        request_data = request.args

    if 'dt_item' in request_data:
        dt_item = request_data['dt_item']
    current_app.logger.info(f'api.download dt_item {dt_item}')

    # # nice idea, but cant return in for loop
    # # convert single dt_item to list
    # if type(dt_item) not in [list]:
    #     dt_item = [dt_item]

    # # create file paths only list from dt_item
    # dt_item_path = []
    # for dt_item_i in dt_item:
    #     dt_item_path += [_['dt_item_path'] for _ in current_app.dt_data_list if _['dt_item'] == dt_item_i]
    #        current_app.logger.info(f'api.autoedit dt_item_path {dt_item_path}')

    # # for path in dt_item_path:

    dt_item_path = [_['dt_item_path'] for _ in current_app.dt_data_list if _['dt_item'] == dt_item][-1]
    current_app.logger.info(f'api.download dt_item_path {dt_item_path}')
    return send_from_directory(
        os.path.dirname(dt_item_path),
        os.path.basename(dt_item_path),
        as_attachment=True
    )
