from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/echo", methods=['GET'])
def echoer():
	#return "This is an echo."
	# Accessed via localhost:8080?msg=foo
	return request.args.get('msg')

if __name__ == '__main__':
	# 0.0.0.0 is ALL interfaces (on the container)
	# So, listen for ALL incoming network traffic.	
	app.run(host='0.0.0.0',port=8080)
