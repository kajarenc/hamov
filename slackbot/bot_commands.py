import json
import os


def handle_start(request_dict):
    trigger_id = request_dict.get('trigger_id')
    if trigger_id:
        request_dict['orders'] = []
        filename = '{name}.json'.format(name=trigger_id.replace('.', '-'))
        path = os.path.join(os.getcwd(), 'orders', filename)
        print(path)
        with open(path, 'w') as outfile:
            json.dump(request_dict, outfile)
    return True
