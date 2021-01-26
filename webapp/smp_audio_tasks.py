# import sys
# sys.path.append('/home/ub/code/smp_audio')

# from argparse import Namespace
from smp_audio.autoedit import autoedit_conf_default
from smp_audio.autoedit import main_autoedit

from smp_audio.autocover import autocover_conf_default
from smp_audio.autocover import main_autocover

from smp_audio.automaster import automaster_conf_default
from smp_audio.automaster import main_automaster

from smp_audio.common import autofilename, ns2kw, kw2ns

def run_autoedit_2(*args, **kwargs):
    # print(f'run_autoedit args_ns {args_ns}')

    args_ns = kwargs['autoedit_conf']
    autoedit_res = main_autoedit(args_ns)
        
    # print(f'run_autoedit res {autoedit_res}')
    
    return autoedit_res
