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

from .smp_audio_tasks import autofilename
from .smp_audio_tasks import ns2kw, kw2ns
from .smp_audio_tasks import run_autoedit_2, autoedit_conf_default
from .smp_audio_tasks import main_autocover, autocover_conf_default
from .smp_audio_tasks import main_automaster, automaster_conf_default

from .api import authenticate, not_authorized
from .api import api_response_ok, api_response_started, api_response_error

api_smp = Blueprint('api/smp', __name__)

@api_smp.before_request
def authenticate() -> Optional[Response]:
    """
    verify token, bind user to request global
    """
    token = request.headers.get('X-Authentication')
    current_app.logger.info(f'api.authenticate token = {token}')
    if token:
        g.user = User.find_by_api_key(token)
        if g.user:
            return None
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
def process_create_pid_file(process, args):
    filename = os.path.join(args.rootdir, 'data', args.mode, args.filename_export[:-4])
    filename += '.pid'
    f = open(filename, 'w')
    f.write(f'{process.name}/{process.pid}')
    f.close()
    return filename

def input_filenames_exist(filenames):
    return [os.path.join(g.user.home_directory, filename) for filename in filenames if os.path.exists(os.path.join(g.user.home_directory, filename))]

############################################################
# autoedit
def autoedit_GET():
    return api_response_ok({
        'message': 'autoedit help',
        'data': {
            'name': 'autoedit',
            'conf': autoedit_conf_default,
        }
    })

def autoedit_POST():
    # request
    # configure and run autoedit
    autoedit_conf = kw2ns(autoedit_conf_default)
    current_app.logger.info(f'api_smp.autoedit_POST autoedit_conf_default {autoedit_conf}')

    # request data copy to configuration
    request_data = request.json
    for k in autoedit_conf_default:
        k_req = f'{k}'
        if k_req in request_data:
            v_req = request_data[k_req]
            setattr(autoedit_conf, k, v_req)

    # configuration post-process
    autoedit_conf.rootdir = g.user.home_directory
    autoedit_conf.filenames = input_filenames_exist(autoedit_conf.filenames)
    autoedit_conf.filename_export = autofilename(autoedit_conf)
            
    current_app.logger.info(f'api_smp.autoedit_POST autoedit_conf_request {autoedit_conf}')
    
    # function map request
    # create process with computation = heavy 
    # heavy = anything taking more than a few seconds
    heavy_process = Process(
        target=run_autoedit_2, # my_func
        kwargs={
            'autoedit_conf': autoedit_conf,
        },
        daemon=True,
    )
    heavy_process.start()
    # create pid file in work dir
    processhandle = process_create_pid_file(heavy_process, autoedit_conf)
    # response
    return api_response_started({
        'message': 'autoedit started',
        'data': {
            # function
            'name': 'autoedit',
            # input arguments
            'conf': ns2kw(autoedit_conf),
            # output returned
            'processhandle': processhandle,
            'location': os.path.join(
                os.path.basename(autoedit_conf.filename_export)
            ),
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

############################################################
# autocover / autofeature
def autocover_GET():
    return api_response_ok({
        'message': 'autocover help',
        # output returned
        'data': {
            # function
            'name': 'autocover',
            # input arguments
            'conf': autocover_conf_default,
        }
    })

def autocover_POST():
    # configure and run autocover
    autocover_conf = kw2ns(autocover_conf_default)
    current_app.logger.info(f'api_smp.autocover_POST autocover_conf_default {autocover_conf}')

    # request data copy to configuration
    request_data = request.json
    for k in autocover_conf_default:
        k_req = f'{k}'
        if k_req in request_data:
            v_req = request_data[k_req]
            setattr(autocover_conf, k, v_req)

    # configuration post-process
    autocover_conf.rootdir = g.user.home_directory
    autocover_conf.filenames = input_filenames_exist(autocover_conf.filenames)
    autocover_conf.filename_export = autofilename(autocover_conf)
            
    current_app.logger.info(f'api_smp.autocover_POST autocover_conf_request {autocover_conf}')
    
    # Create a process with "heavy" computation
    # anything taking more than a few seconds
    # heavy_process = Process(
    #     target=main_autocover, # my_func
    #     args=[autocover_conf],
    #     # kwargs={
    #     #     'autocover_conf': autocover_conf,
    #     # },
    #     daemon=True,
    # )
    # heavy_process.start()
    # return api_response_started({
    #     'message': 'autocover started',
    # })

    heavy_process = Process(
        target=main_autocover,
        args=[autocover_conf],
        daemon=True,
    )
    heavy_process.start()
    # create pid file in work dir
    processhandle = process_create_pid_file(heavy_process, autocover_conf)
    
    # response
    return api_response_started({
        'message': 'autocover started',
        # output returned
        'data': {
            # function
            'name': 'autocover',
            # input arguments
            'conf': ns2kw(autocover_conf),
            'processhandle': processhandle,
            'location': os.path.join(
                os.path.basename(autocover_conf.filename_export)
            ),
        }
    })


@api_smp.route('/autocover', methods=['GET', 'POST'])
def autocover() -> Response:
    """autocover

    Run autocover from request data
    - GET: return help / default conf
    - POST: run autocover with request conf
    """
    if request.method == 'GET':
        res = autocover_GET()
    elif request.method == 'POST':
        res = autocover_POST()
    return res

############################################################
# automaster
def automaster_GET():
    # location = ""
    return api_response_ok({
        'message': 'automaster help',
        # output returned
        'data': {
            # function
            'name': 'automaster',
            # input arguments as help
            'conf':automaster_conf_default,
        }
    })

def automaster_POST():
    # configure and run automaster
    automaster_conf = kw2ns(automaster_conf_default)
    current_app.logger.info(f'api_smp.automaster_POST automaster_conf_default {automaster_conf}')

    # request data copy to configuration
    request_data = request.json
    for k in automaster_conf_default:
        k_req = f'{k}'
        if k_req in request_data:
            v_req = request_data[k_req]
            setattr(automaster_conf, k, v_req)

    # configuration post-process
    automaster_conf.rootdir = g.user.home_directory
    automaster_conf.filenames = input_filenames_exist(automaster_conf.filenames) # [os.path.join(g.user.home_directory, filename) for filename in automaster_conf.filenames]
    automaster_conf.references = input_filenames_exist(automaster_conf.references) # [os.path.join(g.user.home_directory, reference) for reference in automaster_conf.references]
    
    current_app.logger.info(f'api_smp.automaster_POST automaster_conf_request {automaster_conf}')

    if len(automaster_conf.filenames) < 1:
        return api_response_error({
            'message': 'no input file found',
        })
    
    automaster_conf.filename_export = autofilename(automaster_conf)
    
    heavy_process = Process(
        target=main_automaster,
        args=[automaster_conf],
        daemon=True,
    )
    heavy_process.start()
    
    # TODO: create pid file in work dir by app context
    processhandle = process_create_pid_file(heavy_process, automaster_conf)
    
    # res = main_automaster(automaster_conf)
    return api_response_started({
        'message': 'automaster started',
            # output returned
        'data': {
            # function
            'name': 'automaster',
            # input arguments
            'conf': ns2kw(automaster_conf),
            'processhandle': processhandle,
            'location': os.path.join(
                # 'data',
                os.path.basename(automaster_conf.filename_export)
            ),
        }
    })

@api_smp.route('/automaster', methods=['GET', 'POST'])
def automaster() -> Response:
    """automaster

    Run automaster from request data
    - GET: return help / default conf
    - POST: run automaster with request conf
    """
    if request.method == 'GET':
        res = automaster_GET()
    elif request.method == 'POST':
        res = automaster_POST()
    return res


# # get directory tree listing
# @api_smp.route('/files/<string:filename>', methods=['GET'])
# def download(filename: str) -> Response:
#     """
#     Retrieve stored file
#     """
#     current_app.logger.info(f'download filename {filename}')
#     filepath = os.path.join(
#         g.user.home_directory,
#         filename
#     )
#     if os.path.isdir(filepath):
#         # return dir listing
#         dirlist = [{
#             'filepath': os.path.join(filepath, _)} for _ in os.listdir(filepath)]
#         return api_response_ok({
#             'message': 'directory',
#             'dirlist': dirlist,
#         })
#     elif os.path.isfile(filepath):
#         return send_from_directory(
#             g.user.home_directory,
#             filename,
#             as_attachment=True
#         )


# @api_smp.route('/item', methods=['GET', 'POST'])
# def item() -> Response:
#     """
#     Accept soundfile url
#     """
#     # default dt_item
#     dt_item = 'default'
#     if request.method == 'POST':
#         request_data = request.form
#         # current_app.logger.info(f'item request.form {list(request.form.keys())}')

#         # if 'dt_item' in request.form:
#         #     dt_item = request.form['dt_item']
#         # elif 'dt_item' not in request.form and 'dt_session' in request.form:
#         #     dt_item = request.form['dt_session']
#     elif request.method == 'GET':
#         request_data = request.args
#         # current_app.logger.info(f'item request.form {list(request.form.keys())}')

#         # if 'dt_item' in request.args:
#         #     dt_item = request.args['dt_item']
#         # elif 'dt_item' not in request.args and 'dt_session' in request.args:
#         #     dt_item = request.args['dt_session']

#     if 'dt_item' in request_data:
#         dt_item = request_data['dt_item']
#     elif 'dt_item' not in request_data and 'dt_session' in request_data:
#         dt_item = request_data['dt_session']

#     #     url = request.json.get('url')
#     #     if validate_url(url):
#     #         current_app.queue.send(url)
#     #         return api_response_ok({'message': 'Url accepted'})
#     #     else:
#     #         return api_response_error({'message': 'Invalid url'})
#     # return Response(status=405)

#     current_app.logger.info(f'api_smp.item requested dt_item {dt_item}')

#     # # do the work and get the item
#     # if dt_item in current_app.dt_data:
#     #     dt_item_path = current_app.dt_data[dt_item]['path']
#     #     current_app.logger.info(f'item dt_item[path] {dt_item_path}')
#     # else:
#     #     dt_item_path = "None"
        
#     # do the work and get the item
#     # if dt_item in current_app.dt_data:
#     dt_item_dict = [_ for _ in current_app.dt_data_list if _['dt_item'] == dt_item]
#     if len(dt_item_dict) > 0:
#         # dt_item_path = current_app.dt_data[dt_item]['path']
#         dt_item_path = dt_item_dict[-1]['dt_item_path']
#         current_app.logger.info(f'item dt_item[path] {dt_item_path}')
#     else:
#         dt_item_path = "None"
        
#     # item content
#     if os.path.isdir(dt_item_path):
#         # dt_item_content = dict([(dt_item + "_" + _, os.path.join(dt_item_path, _)) for _ in os.listdir(dt_item_path)])
#         dt_item_content = [{
#             'dt_item': os.path.join(dt_item, _),
#             'dt_item_path': os.path.join(dt_item_path, _)} for _ in os.listdir(dt_item_path)]
#     elif os.path.isfile(dt_item_path):
#         # dt_item_copy = [_ for _ in current_app.dt_data if _ == dt_item][0]
#         dt_item_copy = dt_item_dict[-1]['dt_item']
#         dt_item_content = [{
#             'size': os.path.getsize(dt_item_path),
#             # 'dt_item': dt_item,
#             'dt_item_copy': dt_item_copy,
#         }]
#         # dt_item_content = [os.path.join(dt_item_path, _) for _ in  os.listdir(dt_item_path)]
#     else:
#         dt_item_content = []
    
#     return api_response_ok({
#         'message': 'item OK',
#         'dt_item': dt_item,
#         'dt_item_content': dt_item_content,
#     })
