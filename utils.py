# Add usual functions that we use a lot
import json

def load_json(file_path):

    with open(file_path) as f:
        d = json.load(f)
        return (d)