from flask import Flask, request
import random
import string

app = Flask(__name__)

fundata = {}  # {roomid:[poss, move]}


@app.route('/sendmove', methods=['POST'])
def testdata():
    print(request.args.get('roomid'))
    return 'ok'


@app.route('/receive', methods=['POST'])
def receive():
    rid = request.args.get('roomid')
    return fundata[rid]


@app.route('/creategame', methods=['GET'])
def savegame():
    for i in range(6):
        newroom = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if newroom not in fundata.keys():
            fundata[newroom] = [[], 'r']
            return newroom
    return None


@app.route('/')
def index():
    return "<html><body><h1>Welcome. Website is running.</h1></body></html>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345, debug=True)
