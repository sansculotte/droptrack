

def run_autoedit_2(*args, **kwargs):
    
    # # check session cookie
    # session_dict = session_init()
    # username = session_dict['username']

    # assert 'username' in request.cookies, 'Require username, please restart app from root level'
    
    print(f'autoedit args {type(args)}')
    print(f'autoedit kwargs {type(kwargs)}')
    
    # print(f'autoedit request {dir(request)}')
    # print(f'autoedit request {request.json}')
    # print(f'autoedit request {request.form}')

    # import main_autoedit
    from smp_audio.autoedit import main_autoedit

    # create argparse.Namespace from request.form
    from argparse import Namespace
    args_ns = Namespace()
    # run main_autoedit with args
    
    # for k in request.form:
    #     setattr(args_ns, k, request.form[k])
    for k in kwargs:
        setattr(args_ns, k, kwargs[k])

    args_ns.numsegs = int(args_ns.numsegs)
    args_ns.seed = int(args_ns.seed)
    args_ns.duration = int(args_ns.duration)
    # args_ns.verbose = False

    # # tracklist = pd.read_csv('{0}_{1}.csv'.format(data_conf['trackstore_filename_base'], username))
    # tracklist_filename = '{0}_{1}.csv'.format(data_conf['trackstore_filename_base'], username)
    # tracklist = data_init(data_conf['trackstore_columns'], tracklist_filename)
    
    # trackid = int(request.form.get('trackid'))
    # # track = tracklist.loc[trackid]
    # # print(f'    run_autoedit track {track}')
    # track = tracklist[tracklist['id'] == trackid].squeeze()
    # print(f'    run_autoedit track {track}')

    # filename = track.filename
    # args_ns.filenames = [track.filepath]
        
    # args_ns.filenames = [track.filepath]
    args_ns.mode = 'autoedit'
    args_ns.sr_comp=22050
    args_ns.sorter='features_mt_spectral_spread_mean'
    args_ns.seglen_min=2
    args_ns.seglen_max=60
    args_ns.write=False

    # args_ns.assemble_mode = request.form.get('assemble_mode')
    args_ns.assemble_crossfade = 10
    
    print(f'run_autoedit args_ns {args_ns}')

    autoedit_res = main_autoedit(args_ns)
        
    print(f'run_autoedit res {autoedit_res}')
    
    return autoedit_res

