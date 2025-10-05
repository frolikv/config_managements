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
    return vfs

# print(load_vfs("vfs.csv"))