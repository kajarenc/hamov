import json
import requests
import os
from pathlib import Path


def process_order(string):
    tokens = string.split(',')
    results = []
    for token in tokens:
        token = token.strip()
        if '-' in token:
            product_id, amount = token.split('-')
        else:
            product_id, amount = token, '1'
        results.append((product_id, amount))
    return results


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
                orders = process_order(request_dict.get('text'))
                for order, amount in orders:
                    for _ in range(int(amount)):
                        data['orders'].append({
                            'user_id': request_dict.get('user_id'),
                            'text': order
                        })

                with open(file_path, 'w') as outfile:
                    json.dump(data, outfile)
            return True
        else:
            return False


def handle_end(request_dict):
    trigger_id = request_dict.get('trigger_id')
    team_id = request_dict.get('team_id')
    if trigger_id and team_id:
        file_path = get_file_name(team_id)
        if Path(file_path).exists():
            with open(file_path, 'r') as readfile:
                data = json.loads(readfile.read())
                data_for_request = {}
                data_for_request['restaurant_url'] = data['text']
                payload = {}
                for order in data['orders']:
                    if order['user_id'] not in payload:
                        payload[order['user_id']] = [order['text']]
                    else:
                        payload[order['user_id']].append(order['text'])
                data_for_request['orders'] = payload
                data_for_request['telephone'] = '+37455362004'
                data_for_request['delivery_address'] = '3 Moskovyan Street'
                data_for_request['house'] = ''
                data_for_request['apartment'] = ''
                data_for_request['address_details'] = 'Loft'
                data_for_request['comments'] = ''
                requests.post('http://d4bb476b.ngrok.io/orders', json=data_for_request)
