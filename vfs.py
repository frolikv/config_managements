import csv

def load_vfs(csv_path):
    vfs = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row['path']
            type = row['type']
            content = row.get('content', '') if type == 'file' else None
            vfs[path] = {'type': type, 'content': content}
    print(vfs)
    return vfs

def get_children(vfs, path):
    if path[-1] != '/':
        path += '/'
    children = set()
    for el in vfs:
        if el.startswith(path) and el != path.rstrip('/'):
            node = el[len(path):]
            if '/' in node:
                to_add = node.split('/')[0]
                children.add(to_add)
            else:
                children.add(node)
    if ('') in children:
        children.remove('')
    return sorted(children)