''' Load asset.
    asset/ contains four rules txt file provided by project webpage.
    This script load probes (on import) and build a category tree
'''

# global variable:
# category tree
category_root = None


class CategoryNode(object):
    ''' The tree node class, used to build category tree
        Fields:
        name - name of the category, such as "Root"
        queries - list of queries for the category; query is list of keywords
        children - list of sub category nodes
        url_set - document sample urls of the category
    '''
    def __init__(self, name, queries, children):
        self.name = name
        self.queries = queries
        self.children = children
        self.url_set = set()


def on_import():
    ''' initialize two global variables on import
        @reutrn: None
    '''
    global category_root

    if category_root:  # don't load again if category_root is initialized
        return

    print 'load assets...',

    # load assets
    probes_map = {}
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

    # initialize category tree
    category_root = CategoryNode('Root', [], [
        CategoryNode('Computers', probes_map['Computers'], [
            CategoryNode('Hardware', probes_map['Hardware'], []),
            CategoryNode('Programming', probes_map['Programming'], [])
        ]),
        CategoryNode('Health', probes_map['Health'], [
            CategoryNode('Diseases', probes_map['Diseases'], []),
            CategoryNode('Fitness', probes_map['Fitness'], [])
        ]),
        CategoryNode('Sports', probes_map['Sports'], [
            CategoryNode('Soccer', probes_map['Soccer'], []),
            CategoryNode('Basketball', probes_map['Basketball'], []),
        ])
    ])

    print 'done.'


on_import()
