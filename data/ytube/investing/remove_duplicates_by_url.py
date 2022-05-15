# read yt_data.json and remove all duplicates
# and save back to yt_data.json

import json
import os

with open(os.path.join('data', 'ytube', 'investing', 'yt_data.json')) as f:
    data = json.load(f)

new_data = []
for d in data:
    if d not in new_data:
        new_data.append(d)

with open(os.path.join('data', 'ytube', 'investing', 'yt_data.json'), 'w') as f:
    json.dump(new_data, f)