from flask import Flask, jsonify
from flask import request
import os
import json


app = Flask(__name__)

store = {}


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"

# 127.0.0.1:8080/echo?msg="Hey there!"


@app.route("/echo", methods=['GET'])
def echoer():
    # return "This is an echo."
    # Accessed via localhost:8080?msg=foo
    return request.args.get('msg')


MSG_KEY_REPLACED = "Value of existing key replaced"
MSG_KEY_NOT_EXIST = "Key does not exist"
MSG_KEY_CREATED = "New key created"


@app.route("/kvstore/<string:key>", methods=['GET', 'PUT'])
def get_key(key):
    if request.method == 'GET':
        print(key)
        if key in store:
            resp = {"result": "success", "value": str(store[key])}
            return jsonify(resp), 200
        else:
            resp = {"result": "error", "value": MSG_KEY_NOT_EXIST}
            return jsonify(resp), 404

    elif request.method == 'PUT':
        replaced = False
        resp_code = 201
        msg = MSG_KEY_CREATED
        if key in store:
            replaced = True
            resp_code = 200
            msg = MSG_KEY_REPLACED
        store[key] = str(request.data)

        resp = {"replaced": replaced, "msg": msg}
        return jsonify(resp), resp_code
    return


if __name__ == '__main__':
    ip = os.getenv('IP', '0.0.0.0')
    port = os.getenv('PORT', 8080)
    main_ip = os.getenv('MAINIP')
    print(ip, port, main_ip)
    app.run(host=ip, port=port)
