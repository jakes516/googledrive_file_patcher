from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST', 'DELETE'])
def hello_world():
    if request.method == 'GET':
        return 'Hello, World!'

    if request.method == 'POST':
        return request.data



@app.route('/version')
def not_hello_world():
    return str(request.headers)
    return 'Hello, Jake!'

if __name__ == '__main__':
   app.run(port = 12345)
