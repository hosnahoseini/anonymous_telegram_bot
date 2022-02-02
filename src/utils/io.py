import json

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def write_json(path, data, indent=4):
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)