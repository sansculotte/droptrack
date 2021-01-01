# from argparse import Namespace
from smp_audio.util import kw2ns, ns2kw
from smp_audio.autoedit import autoedit_conf_default
from smp_audio.autoedit import main_autoedit

def run_autoedit_2(*args, **kwargs):
    # print(f'run_autoedit args_ns {args_ns}')

    args_ns = kwargs['autoedit_conf']
    autoedit_res = main_autoedit(args_ns)
        
    # print(f'run_autoedit res {autoedit_res}')
    
    return autoedit_res

