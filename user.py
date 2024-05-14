from configs import Color

class User:
    def __init__(self, email, socket = None, interests = ''):
        self.email = email
        self.interests = interests
        self.socket = socket
        self.contacts = {}

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
