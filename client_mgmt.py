import requests

class ClientError(Exception):
    pass

class PingFail(ClientError):
    pass

class ClientNoResponse(ClientError):
    pass

class ClientSideServer:
    def __init__(self, ip, port, scheme, name):
        self.ip = ip
        self.port = port
        self.scheme = scheme
        self.name = name
    
    def make_request(self, method, endpoint, data=None):
        try:
            if method == 'GET':
                r = requests.get('{}://{}:{}{}'.format(self.scheme, self.ip, self.port, endpoint))
            if method == 'POST':
                r = requests.post('{}://{}:{}{}'.format(self.scheme, self.ip, self.port, endpoint), data=data)
        except:
            raise ClientNoResponse('Client failed to respond to request')
        else:
            return r
    
    def ping(self):
        try:
            self.make_request('GET', '/ping')
        except ClientNoResponse:
            ping_pass = False
        else:
            ping_pass = True
        return ping_pass

class ClientMGMT:
    def __init__(self):
        self.clients = {}
    
    def add_client(self, server):
        if server.ping():
            self.clients[server.name] = server
            print('Client {}, {} added to list'.format(server.name, server.ip))
        else:
            raise PingFail('Client did not respond to ping')
    
    def broadcast_to_clients(self, method, endpoint, data=None):
        if not data is None:
            print('Broadcasting message to clients, {} {} {}'.format(method, endpoint, data))
        else:
            print('Broadcasting message to clients, {} {}'.format(method, endpoint))
        new_clients = self.clients
        remove_list = []
        for client in new_clients:
            client = new_clients[client]
            try:
                client.make_request(method, endpoint, data=data)
            except ClientNoResponse:
                print('Client {}, {} did not respond to ping, removing them from the list'.format(client.name, client.ip))
                remove_list.append(client.name)
        
        for name in remove_list:
            self.remove_client(name)

    def remove_client(self, name):
        del self.clients[name]
