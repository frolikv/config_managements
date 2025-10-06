import vfs


def vfs_save(cur_vfs, save_path):
    if not cur_vfs:
        return 1
    with open(save_path, 'w') as new_vfs:
        new_vfs.write("path,type,content")
        for node in cur_vfs:
            new_vfs.write(f"\n{node},{cur_vfs[node]['type']},{'' if cur_vfs[node]['content'] == None else cur_vfs[node]['content']}")
    return 0

def ls(cur_vfs, cur_path):
    res = f"----------\nCurrent path: {cur_path}\n"
    nodes = []
    if cur_path[-1] != '/':
        cur_path += '/'
    if not cur_vfs:
        return ['', 1]
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