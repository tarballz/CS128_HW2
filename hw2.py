#import pdb
import os


import requests
from sanic import Sanic
from sanic.response import text, json, raw
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage


app = Sanic(__name__)

# Error messages
MSG_KEY_REPLACED = "Value of existing key replaced"
MSG_KEY_NOT_EXIST = "Key does not exist"
MSG_KEY_CREATED = "New key created"
MSG_BODY_TO_LARGE = "Object too large. Size limit is 1MB"
MSG_KEY_INVALID_FMT = "Key not valid"
MSG_SERVER_UNAVAILABLE = "Server unavailable"
REQ_BODY_BYTES_LIMIT = 1000000  # 1MB

WORKER_NODE = False

SUCCESS = 'Success'
ERROR = 'Error'

MAINIP = None

# The actual data:
store = {}


@app.route("/")
async def test(request):
    return text('Hello world!')


@app.route("/echo", methods=['GET'])
async def echoer(request):
    # return "This is an echo."
    # Accessed via localhost:8080/echo?msg=foo
    return text(request.args.get('msg'))


class KVStoreView(HTTPMethodView):
    """KVStoreView handles the key:value store functionality needed
    to satisfy the assignment 2 spec for CMPS 128.
    """

    async def get(self, request, key, *args, **kwargs):
        """Used as the `GET` HTTP verb for the kvstore and it also
        semantically `gets` the key (if it exists) or returns an
        error if it does not.

        Args:
            self: KVStoreView instance we are in.
            request: The actual request from the user/client as processed
                by Sanic and given to us.
            key: The key portion of the key:value relationship. In
                this case it's the key for our 'store' dictionary.

        Returns:
            A Sanic Response.json Sanic instance that will be a serialized
                json response to the user/client.
        """
        print(request.content_type)
        if key in store:
            resp = {"result": SUCCESS, "value": store[key]}
            return json(resp, status=200)
        else:
            resp = {"result": ERROR, "msg": MSG_KEY_NOT_EXIST}
            return json(resp, status=404)

    async def put(self, request, key):
        """Used as the `PUT` HTTP verb for the kvstore and it also
        semantically `puts` the key (whether it exists or not) and then states
        whether or not it was replaced as a part of the response.

        Args:
            self: KVStoreView instance we are in.
            request: The actual request from the user/client as processed
                by Sanic and given to us.
            key: The key portion of the key:value relationship. In
                this case it's the key for our 'store' dictionary.

        Returns:
            A Sanic Response.json Sanic instance that will be a serialized
                json response to the user/client.
        """
        replaced = 'False'
        resp_code = 201
        msg = MSG_KEY_CREATED
        if key in store:
            replaced = 'True'
            resp_code = 200
            msg = MSG_KEY_REPLACED
        try:
            store[key] = request.json
        except InvalidUsage:
            store[key] = str(request.body)

        # pdb.set_trace()

        resp = {"replaced": replaced, "msg": msg}
        return json(resp, status=resp_code)

    async def delete(self, request, key):
        if key in store:
            # We could use pop if we had to do anything w/ the value.
            del store[key]
            resp = {"result": SUCCESS}
            return json(resp, status=200)
        else:
            msg = MSG_KEY_NOT_EXIST
            resp = {"result": ERROR, "msg": msg}
            return json(resp, status=404)


async def KVStoreBadKey(badkey, *args, **kwargs):
    # if len(badkey) > 200: 
    #     r = {"result": ERROR, "msg": "Key not valid"}
    #     return json(r, 403)
    r = {"result": ERROR, "msg": "Key not valid"}
    return json(r, status=403)

class KVForwarder(HTTPMethodView):
    
    async def _all(self, req, key):
        """
        Forwards all requests to the primary node aka MAINIP.
            :param request: 
            :param key: 
            :param *args: 
            :param **kwargs: 
        """
        print("*" * 80)
        print(req, key)
        print(MAINIP)
        #response = requests.Request()
        try:
            response = requests.request(url=('http://' + MAINIP + '/kv-store/' + key ), method=req.method)
            print(response)
            if response.json() != None:
                return raw(response.content, response.status_code)
        except requests.exceptions.ConnectionError:
            r = {"result": ERROR, "msg": MSG_SERVER_UNAVAILABLE}
            return json(r, 501)
        return raw(response.content, response.status_code)

    async def get(self, request, key):
        return await self._all(request, key)

    async def put(self, request, key):
        return await self._all(request, key)

    async def delete(self, request, key):
        return await self._all(request, key)


def load_master_routes(*args, **kwargs):
    app.add_route(KVStoreView.as_view(), r"/kv-store/<key:[a-zA-Z0-9_]{1,201}>")
    app.add_route(KVStoreBadKey, r"/kv-store/<badkey>")


def load_forwarder_routes(*args, **kwargs):
    app.add_route(KVForwarder.as_view(), 
            r"/kv-store/<key:[a-zA-Z0-9_]{1,201}>")
    app.add_route(KVStoreBadKey, r"/kv-store/<badkey>")


@app.middleware('request')
async def request_body_limit(request):
    if len(request.body) > REQ_BODY_BYTES_LIMIT:
        return json({"result": ERROR, "msg": MSG_BODY_TO_LARGE}, status=200)


if __name__ == '__main__':
    app.config.KEEP_ALIVE = True
    ip = os.getenv('IP', '0.0.0.0')
    port = os.getenv('PORT', 8080)
    MAINIP = os.getenv('MAINIP', None)
    if (MAINIP != None):
        WORKER_NODE = True
        # verify further?
        load_forwarder_routes()
    else:
        load_master_routes()
    app.run(host=ip, port=port, debug=False)
