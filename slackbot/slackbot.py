from flask import Flask

from flask import Flask, request, make_response, render_template
import json

from flask import Flask, request, make_response, jsonify, Response
from bot_commands import handle_start, handle_order
import os
import json

from slackclient import SlackClient

app = Flask(__name__)


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
            'text': 'GOOD!'
        })
    else:
        return jsonify({
            "response_type": "in_channel",
            'text': 'Something went wrong! :('
        })


if __name__ == '__main__':
    app.run(debug=True)
