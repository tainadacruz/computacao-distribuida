from configs import Color

class User:
    def __init__(self, email, socket = None, interests = ''):
        self.username = email
        self.interests = interests
        self.is_online = False
        self.socket = socket
        self.contacts = {}

    def set_online(self, online):
        self.is_online = online

    def is_user_online(self):
        return self.is_online

    def set_socket(self, socket):
        self.socket = socket # Associa um socket com o usuário para mensagens diretas

    def send_message(self, message):
        if self.is_online and self.socket: # Envia uma mensagem para o usuário se está online e tem um socket
            try:
                self.socket.send_pyobj(message)
                print(f'{Color.YELLOW} mensagem enviada {Color.RESET}')
                return True
            except Exception as e:
                print(e)
                return False
            
        print("User offline ou socket desconectado.")
        return False
    
    
       
    # FUNÇÕES QUE NÃO SERVEM MAIS, MAS DEIXA AÍ NÉ VAI QUE
    
    def serialize(self):
        # Converte User para JSON
        return json.dumps({
            'username': self.username,
            'password': self.password,
            'pull_address': self.pull_address,
            'is_online': self.is_online,
            'socket': self.socket
        })

    def deserialize(data):
        # Converte JSON de volta pra User
        user_data = json.loads(data)
        user = User(user_data['username'], user_data['password'], user_data['pull_address'])
        user.is_online = user_data['is_online']
        return user

    def __repr__(self):
        return f"User({self.username}, Online: {self.is_online})"
