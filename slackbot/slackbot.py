from flask import Flask

from flask import Flask, request, make_response, render_template
import json

from flask import Flask, request, make_response, Response
from bot_commands import handle_start
import os
import json

from slackclient import SlackClient

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Karen!'


@app.route("/start", methods=["POST"])
def start():
    # request_data = json.loads(request.data)
    data = request.form.to_dict()
    handle_start(data)
    return make_response("OK!", 200, {"content_type": "application/json"})


if __name__ == '__main__':
    app.run(debug=True)
