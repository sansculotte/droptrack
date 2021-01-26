"""smp_audio.api_smp
"""
import os
from flask import (
    g,
    current_app,
    request,
    Blueprint,
    Response,
)
from .models import db
from .models import Task

from multiprocessing import Process

from .smp_audio_tasks import autofilename
from .smp_audio_tasks import ns2kw, kw2ns
from .smp_audio_tasks import main_autoedit, autoedit_conf_default
from .smp_audio_tasks import main_autocover, autocover_conf_default
from .smp_audio_tasks import main_automaster, automaster_conf_default

from .api import (
    authenticate,
    api_response_ok,
    api_response_accepted,
    api_response_error
)

api_smp = Blueprint('api_smp', __name__)


api_smp.before_request(authenticate)


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
def input_filenames_exist(filenames):
    return [
        os.path.join(g.user.home_directory, os.path.basename(filename))
        for filename
        in filenames
        if os.path.exists(os.path.join(g.user.home_directory, os.path.basename(filename)))
    ]


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
    # request configure and run autoedit
    autoedit_conf = kw2ns(autoedit_conf_default)
    current_app.logger.info(f'api_smp.autoedit_POST autoedit_conf_default {autoedit_conf}')

    # request data copy to configuration
    request_data = request.json
    # extract filenames from files
    request_data['filenames'] = [f['name'] for f in request_data['files']]
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

    task = Task(
        name=os.path.basename(autoedit_conf.filename_export),
        user=g.user,
    )
    db.session.add(task)
    db.session.commit()

    # function map request
    async_process = Process(
        target=main_autoedit,
        args=[autoedit_conf],
        kwargs={'task': task},
        daemon=True,
    )
    async_process.start()
    # create pid file in work dir
    # response
    return api_response_accepted(task.to_dict(), location=task.url)

    # return api_response_started({
    #     'message': 'autoedit started',
    #     'data': {
    #         # function
    #         'name': 'autoedit',
    #         # input arguments
    #         'conf': ns2kw(autoedit_conf),
    #         # output returned
    #         # 'processhandle': processhandle,
    #         'location': os.path.join(
    #             os.path.basename(autoedit_conf.filename_export + '.wav')
    #         ),
    #         'locations': [os.path.join(
    #             os.path.basename(autoedit_conf.filename_export + '.' + output_type)
    #         ) for output_type in autoedit_conf.outputs],
    #     }
    # })

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

    task = Task(
        name=os.path.basename(autocover_conf.filename_export),
        user=g.user,
    )
    db.session.add(task)
    db.session.commit()

    async_process = Process(
        target=main_autocover,
        args=[autocover_conf],
        kwargs={'task': task},
        daemon=True,
    )
    async_process.start()

    # response
    return api_response_accepted(
        {'message': 'autoedit accepted', 'task': task.to_dict()},
        location=task.url
    )

    # return api_response_started({
    #     'message': 'autocover started',
    #     # output returned
    #     'data': {
    #         # function
    #         'name': 'autocover',
    #         # input arguments
    #         'conf': ns2kw(autocover_conf),
    #         # 'processhandle': processhandle,
    #         'location': os.path.join(
    #             os.path.basename(autocover_conf.filename_export) + '.json'
    #         ),
    #         'locations': [os.path.join(
    #             os.path.basename(autocover_conf.filename_export + '.' + output_type)
    #         ) for output_type in autocover_conf.outputs],
    #     }
    # })


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

    # request data copy to configuration
    request_data = request.json
    for k in automaster_conf_default:
        k_req = f'{k}'
        if k_req in request_data:
            v_req = request_data[k_req]
            setattr(automaster_conf, k, v_req)

    current_app.logger.info(f'api_smp.automaster_POST automaster_conf {automaster_conf}')

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

    task = Task(
        name=os.path.basename(automaster_conf.filename_export),
        user=g.user,
    )
    db.session.add(task)
    db.session.commit()

    async_process = Process(
        target=main_automaster,
        args=[automaster_conf],
        kwargs={'task': task},
        daemon=True,
    )
    async_process.start()

    # processhandle = process_create_pid_file(async_process, automaster_conf)

    # res = main_automaster(automaster_conf)
    return api_response_accepted(
        {'message': 'automaster accepted', 'task': task.to_dict()},
        location=task.url
    )

    #     # output returned
    #     'data': {
    #         # function
    #         'name': 'automaster',
    #         # input arguments
    #         'conf': ns2kw(automaster_conf),
    #         # 'processhandle': processhandle,
    #         'location': os.path.join(
    #             # 'data',
    #             os.path.basename(automaster_conf.filename_export) + '.wav'
    #         ),
    #         'locations': [os.path.join(
    #             os.path.basename(automaster_conf.filename_export + '.' + output_type)
    #         ) for output_type in automaster_conf.outputs],
    #     }
    # })

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
