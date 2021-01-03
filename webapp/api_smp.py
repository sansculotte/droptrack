"""smp_audio.api_smp
"""
import os
from typing import Optional
from flask import (
    g,
    current_app,
    json,
    request,
    jsonify,
    url_for,
    session,
    send_from_directory,
    Blueprint,
    Response,
)
from .models import User

from .filesys import walkdirlist

from multiprocessing import Process

from .smp_audio_tasks import ns2kw, kw2ns
from .smp_audio_tasks import run_autoedit_2, autoedit_conf_default

from .api import authenticate, not_authorized
from .api import api_response_ok, api_response_started, api_response_error

api_smp = Blueprint('api/smp', __name__)

@api_smp.before_request
def authenticate() -> Optional[Response]:
    """
    verify token, bind user to request global
    """
    token = request.headers.get('X-Authentication')
    if token:
        g.user = User.verify_api_token(token)
        return None
    else:
        return not_authorized()


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
def autoedit_POST():
    # configure and run autoedit
    autoedit_conf = kw2ns(autoedit_conf_default)
    current_app.logger.info(f'api_smp.autoedit_POST autoedit_conf_default {autoedit_conf}')

    request_data = request.json
    for k in autoedit_conf_default:
        k_req = f'{k}'
        if k_req in request_data:
            v_req = request_data[k_req]
            setattr(autoedit_conf, k, v_req)

    autoedit_conf.filenames = [os.path.join(g.user.home_directory, filename) for filename in autoedit_conf.filenames]
            
    current_app.logger.info(f'api_smp.autoedit_POST autoedit_conf_request {autoedit_conf}')
    
    # Create a process with "heavy" computation
    # anything taking more than a few seconds
    heavy_process = Process(
        target=run_autoedit_2, # my_func
        # args=autoedit_conf,
        kwargs={
            'autoedit_conf': autoedit_conf,
        },
        daemon=True,
    )
    heavy_process.start()
    return api_response_started({
        'message': 'autoedit started',
    })

def autoedit_GET():
    return api_response_ok({
        'message': 'autoedit help',
        'autoedit': {
            'default': autoedit_conf_default,
        }
    })

@api_smp.route('/autoedit', methods=['GET', 'POST'])
def autoedit() -> Response:
    """autoedit

    Run autoedit from request data
    - GET: return help / default conf
    - POST: run autoedit with request conf
    """
    if request.method == 'GET':
        res = autoedit_GET()
    elif request.method == 'POST':
        res = autoedit_POST()
    return res

# async testing, define some heavy function
def my_func(**kwargs):
    import time
    current_app.logger.info(f"my_func Process start with {kwargs}")
    time.sleep(3)
    current_app.logger.info("my_func Process finished")

# get directory listings
@api_smp.route('/files/<string:filename>', methods=['GET'])
def download(filename: str) -> Response:
    """
    Retrieve stored file
    """
    current_app.logger.info(f'download filename {filename}')
    filepath = os.path.join(
        g.user.home_directory,
        filename
    )
    if os.path.isdir(filepath):
        # return dir listing
        dirlist = [{
            'filepath': os.path.join(filepath, _)} for _ in os.listdir(filepath)]
        return api_response_ok({
            'message': 'directory',
            'dirlist': dirlist,
        })
    elif os.path.isfile(filepath):
        return send_from_directory(
            g.user.home_directory,
            filename,
            as_attachment=True
        )


@api_smp.route('/item', methods=['GET', 'POST'])
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

    current_app.logger.info(f'api_smp.item requested dt_item {dt_item}')

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


