def vfs_save(vfs, save_path):
    if not vfs:
        return -1
    with open(save_path, 'w') as new_vfs:
        new_vfs.write("path,type,content")
        for node in vfs:
            new_vfs.write(f"\n{node},{vfs[node]['type']},{'' if vfs[node]['content'] == None else vfs[node]['content']}")
    return 0