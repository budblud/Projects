from flask import Flask, jsonify, request

app = Flask(__name__)

store = [
    {
        'name': 'My wonderful Store',
        'items': [
            {
                'name': 'My item',
                'price': 15.99
            }
         ]
    }
]

#POST - used to receive data
#GET - used to send data back only

#POST /store data: {name:}
@app.route ('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()

'''#GET /store/<strings:name>
@app.route('/<strings:name>')
def get_store(name):
    pass'''

#GET /store
@app.route('/store')
def get_stores():
    return jsonify({'store': store})

'''#GET /store/<strings:name>/item
@app.route('/<strings:name>/item', methods= ['POST'])
def create_item_in_store(name):
    pass'''

'''#GET /store/<strings:name>/item
@app.route('/<strings:name>/item')
def get_item_in_store(name):
    pass'''

app.run(port=5000)