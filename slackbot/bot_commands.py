import json
import os
from pathlib import Path


def get_file_name(team_id):
    filename = '{name}.json'.format(name=team_id)
    path = os.path.join(os.getcwd(), 'orders', filename)
    return path


def handle_start(request_dict):
    trigger_id = request_dict.get('trigger_id')
    team_id = request_dict.get('team_id')
    if trigger_id and team_id:
        request_dict['orders'] = []
        file_path = get_file_name(team_id)
        with open(file_path, 'w') as outfile:
            json.dump(request_dict, outfile)
    return True


def handle_order(request_dict):
    trigger_id = request_dict.get('trigger_id')
    team_id = request_dict.get('team_id')
    text = request_dict.get('text')
    if trigger_id and team_id and text:
        file_path = get_file_name(team_id)
        if Path(file_path).exists():
            data = None
            with open(file_path, 'r') as readfile:
                data = json.loads(readfile.read())
            if data:
                print("DATA READEDQ!!!!!!")
                print(data)
                data['orders'].append({
                    'user_id': request_dict.get('user_id'),
                    'text': request_dict.get('text')
                })

                with open(file_path, 'w') as outfile:
                    json.dump(data, outfile)
            return True
        else:
            return False
