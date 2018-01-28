from flask import Flask

from flask import Flask, request, make_response, render_template
import json

from flask import Flask, request, make_response, jsonify, Response
from bot_commands import handle_start, handle_order, handle_end
import secrets
import os
import json

from slackclient import SlackClient

app = Flask(__name__)

SLACK_CLIENT_ID = secrets.SLACK_CLIENT_ID
CLIENT_SECRET = secrets.CLIENT_SECRET
VERIFICATION_TOKEN = secrets.VERIFICATION_TOKEN


@app.route('/')
def hello_world():
    return 'Hello Karen!'


@app.route("/start", methods=["POST"])
def start():
    data = request.form.to_dict()
    handle_start(data)
    return jsonify({
        "response_type": "in_channel",
        'text': 'OK, Let\'s start'
    })


@app.route("/order", methods=["POST"])
def order():
    data = request.form.to_dict()
    if handle_order(data):
        return jsonify({
            "response_type": "in_channel",
            'text': 'Got it!'
        })
    else:
        return jsonify({
            "response_type": "in_channel",
            'text': 'Something went wrong! :('
        })


@app.route("/end", methods=["POST"])
def end():
    data = request.form.to_dict()
    handle_end(data)
    return jsonify({
        "response_type": "in_channel",
        'text': 'ok ok, your order is in progress...!'
    })


@app.route("/done", methods=["POST"])
def done():
    slack_client = SlackClient('xoxa-305197754224-305206629728-305206629808-b6fff71346fc6fed1cfe2bd9cfa79336')
    post_message = slack_client.api_call("chat.postMessage", channel="C8ZQRAH1S", text="DONE!!!")
    return jsonify({"text": "OK"})


if __name__ == '__main__':
    app.run(debug=True)
