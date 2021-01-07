"""droptrack.filesys

filesystem related stuff

scan directory trees into list or dict of dictionaries
"""
import os 
from pprint import pprint

def set_leaf(tree, branches, leaf):
    """ Set a terminal element to *leaf* within nested dictionaries.              
    *branches* defines the path through dictionnaries.                            

    Example:                                                                      
    >>> t = {}                                                                    
    >>> set_leaf(t, ['b1','b2','b3'], 'new_leaf')                                 
    >>> print t                                                                   
    {'b1': {'b2': {'b3': 'new_leaf'}}}                                             
    """
    if len(branches) == 1:
        tree[branches[0]] = leaf
        return
    if branches[0] not in tree:
        tree[branches[0]] = {}
    set_leaf(tree[branches[0]], branches[1:], leaf)

def walkdir(startpath):
    """walkdir

    Walk the directory tree from startpath and return as nested dict
    of dicts
    """
    tree = {}
    for root, dirs, files in os.walk(startpath):
        branches = [startpath]
        if root != startpath:
            branches.extend(os.path.relpath(root, startpath).split('/'))

        set_leaf(tree, branches, dict([(d,{}) for d in dirs]+ \
                                      [(f,None) for f in files]))

    return tree

def walkdirlist(startpath, absroot='./', verbose=False):
    """walkdirlist

    Walk the directory tree from startpath and return as flat list of
    dicts. Each dict has at least a short handle and the full path to
    the file, mapping handles to files.
    """
    tree = []
    # print(f'walking startpath {startpath}')
    # startpath basename
    for root, dirs, files in os.walk(startpath):
        if verbose:
            print(f'walking root {root}, dirs {dirs}, files {files}')
        # if len(files) < 1:
        #     continue
        for itempath in dirs + files:
            # if f == 'data':
            #     continue
            itemhandle = os.path.join(root.replace(startpath, ''), itempath)
            if itemhandle.startswith('/'):
                itemhandle = itemhandle[1:]
            # itemhandle = itempath
            if verbose:
                print(f'    itemhandle {itemhandle}')
            itempath = os.path.join(startpath, itemhandle)
            if os.path.isdir(itempath):
                itemtype = 'd'
            elif os.path.isfile(itempath):
                itemtype = 'f'
            tree.append({
                # TODO: map filesys.h struct
                'handle': itemhandle,
                'path': itempath,
                'type': itemtype,
                # 'dt_item_path': os.path.join(absroot, startpath, filepath),
            })
    return tree

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        startpath = sys.argv[1]
    else:
        startpath = '.'

    print(f'filesys walking directory {startpath}')

    # tree = walkdir(startpath)
    tree = walkdirlist(startpath)
    
    print('tree:')
    pprint(tree)
