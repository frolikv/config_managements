import vfs


def vfs_save(cur_vfs, save_path):
    if not cur_vfs:
        return 1
    with open(save_path, 'w') as new_vfs:
        new_vfs.write("path,type,content")
        for node in cur_vfs:
            new_vfs.write(f"\n{node},{cur_vfs[node]['type']},{'' if cur_vfs[node]['content'] == None else cur_vfs[node]['content']}")
    return 0

def ls(cur_vfs, cur_path = ''):
    if not cur_vfs:
        return ['', 1]
    if cur_path[-1] != '/':
        cur_path += '/'
    res = f"----------\nCurrent path: {cur_path}\n"
    nodes = []
    if cur_path != "/":
        res += "\n.."
    for el in vfs.get_children(cur_vfs, cur_path):
        if cur_vfs[f"{cur_path}{el}"]['type'] == 'dir':
            nodes.append(f"/{el}")
        else:
            nodes.append(el)
    for node in sorted(nodes):
        res += f"\n{node}"
    res += "\n----------"
    return [res, 0]

def cd(cur_vfs, cur_path = '', to_go = ''):
    if not cur_vfs:
        return ['', 1, None]
    if cur_path[-1] != '/':
        cur_path += '/'
    if to_go[-1] != '/':
        to_go += '/'

    print(to_go)
    if to_go == '../':
        if cur_path == '/':
            return [f'Invalid path', 1, cur_path]
        parent = cur_path[:-1]
        parent = parent[:parent.rfind('/')]
        print("\t" + parent)
        return [f'Current path is {parent}/', 1, parent]

    if to_go == '/':
        return [f'Current path is {to_go}', 0, to_go]
    if to_go[0] == '/':
        if to_go[:-1] in cur_vfs.keys() and cur_vfs[to_go[:-1]]['type'] == 'dir':
            return [f'Current path is {to_go}', 0, to_go]
        else:
            return [f'Invalid path - {to_go}', 1, cur_path]
    else:
        # print(to_go[:-1])
        # print(vfs.get_children(cur_vfs, f"{cur_path}"))

        if (to_go[:-1] in vfs.get_children(cur_vfs, f"{cur_path}")
                and cur_vfs[f"{cur_path}{to_go[:-1]}"]['type'] == 'dir'):
            return [f'Current path is {cur_path}{to_go}', 0, f"{cur_path}{to_go}"]
        else:
            return [f'Invalid path - {cur_path}{to_go}', 1, cur_path]
