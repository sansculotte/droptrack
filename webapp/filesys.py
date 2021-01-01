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
    tree = {}
    for root, dirs, files in os.walk(startpath):
        branches = [startpath]
        if root != startpath:
            branches.extend(os.path.relpath(root, startpath).split('/'))

        set_leaf(tree, branches, dict([(d,{}) for d in dirs]+ \
                                      [(f,None) for f in files]))

    return tree

def walkdirlist(startpath, absroot='./', verbose=False):
    tree = []
    # startpath basename
    for root, dirs, files in os.walk(startpath):
        # print(f'walking root {root}, dirs {dirs}, files {files}')
        # if len(files) < 1:
        #     continue
        for f in dirs + files:
            # if f == 'data':
            #     continue
            filepath = os.path.join(root.replace('data/dt_sessions/', ''), f)
            if verbose:
                print(f'file {filepath}')
            tree.append({
                'dt_item': filepath,
                'dt_item_path': os.path.join(absroot, filepath),
            })
    return tree

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        startpath = sys.argv[1]
    else:
        startpath = '.'

    print(f'walking directory {startpath}')

    # tree = walkdir(startpath)
    tree = walkdirlist(startpath)
    
    print('tree:')
    pprint(tree)
