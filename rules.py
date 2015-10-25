fnames = ['root.txt', 'computers.txt', 'health.txt', 'sports.txt']

probes_map = {}

for fname in fnames:
    with open(fname, 'r') as fin:
        for lin in fin:
            line = lin.strip()
            words = line.split()
            category = words[0]
            probe = words[1:]
            if category not in probes_map:
                probes_map[category] = [probe]
            else:
                probes_map[category].append(probe)

category_tree = {
    'Root': {
        'Computers': {
            'Hardware': {},
            'Programming': {}
        },
        'Health': {
            'Diseases': {},
            'Fitness': {}
        },
        'Sports': {
            'Soccer': {},
            'Basketball': {}
        }
    }
}

# print probes_map
