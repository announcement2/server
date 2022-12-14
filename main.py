from flask import Flask, jsonify, request
import client_mgmt

app = Flask(__name__)
clients = client_mgmt.ClientMGMT()

@app.errorhandler(400)
def handle400(e):
    return jsonify({
        'code': 400,
        'message': 'Generic 400 Message, this could mean that something has gone wrong in the client program that has to do with sending an HTTP request. This message does not have anything to do with the function of the announcement system.'
    })

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/add_client', methods=['POST'])
def add_client():
    server = client_mgmt.ClientSideServer(request.remote_addr, request.form['server_port'], request.form['server_scheme'], request.form['name'])
    try:
        clients.add_client(server)
    except client_mgmt.PingFail:
        return jsonify({
            'code': 400,
            'message': 'Client server did not respond to a ping.'
        }), 400
    
    return jsonify(
        {
            'code': 200,
            'message': 'Client added to list'
        }
    )

@app.route('/make_announcement', methods=['POST'])
def make_announcement():
    name_id = request.form['name_id']
    name = request.form['name']
    try:
        client = clients.clients[name_id]
    except:
        return jsonify({
            'code': 400,
            'message': "Client did not return a valid name id."
        }), 400

    clients.broadcast_to_clients('POST', '/announcement', data={
        'message': request.form['message'],
        'from': name
    })

    return jsonify(
        {
            'code': 200,
            'message': 'OK'
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4597)
