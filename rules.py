''' Load asset.
    asset/ contains four rules txt file provided by project webpage.
    This script load probes (on import) and build a category tree
'''

# global variables:

# probes for each category.
probes_map = {}

# category tree.
category_root = None


class CategoryNode(object):
    ''' The tree node class, used to build category tree
    '''
    def __init__(self, name, children):
        self.name = name
        self.children = children


def on_import():
    ''' initialize two global variables on import
    '''
    global category_root, probes_map

    if len(probes_map) > 0:  # don't load again if probes_map is loaded
        return

    print 'on_import'

    # initialize category tree
    category_root = CategoryNode('Root', [
        CategoryNode('Computers', [
            CategoryNode('Hardware', []),
            CategoryNode('Programming', [])
        ]),
        CategoryNode('Health', [
            CategoryNode('Diseases', []),
            CategoryNode('Fitness', [])
        ]),
        CategoryNode('Sports', [
            CategoryNode('Soccer', []),
            CategoryNode('Basketball', []),
        ])
    ])

    # load assets
    fnames = ['root.txt', 'computers.txt', 'health.txt', 'sports.txt']
    for fname in fnames:
        path = 'asset/' + fname
        with open(path, 'r') as fin:
            for lin in fin:
                line = lin.strip()
                words = line.split()
                category = words[0]
                probe = words[1:]
                if category not in probes_map:
                    probes_map[category] = [probe]
                else:
                    probes_map[category].append(probe)


on_import()
