import zmq

class Client:
    def __init__(self):
        self.context_sub = zmq.Context()
        self.socket_sub = self.context_sub.socket(zmq.SUB)
        self.socket_sub.connect("tcp://localhost:5556")
        self.context_resp = zmq.Context()
        self.socket_resp = self.context_resp.socket(zmq.REQ)
        self.socket_resp.connect("tcp://localhost:5557")  # Assuming server is listening on port 5557
        #socket_resp.send_string(f"Received registration confirmation for client {client_id}")
        self.context_push = zmq.Context()
        self.socket_push = self.context_push.socket(zmq.PUSH)
        #ele faz a conexão pra enviar a mensagem conforme definido o destinatário então da pra deixar sem conexão por enquanto
        self.context_pull = zmq.Context()
        self.socket_pull = self.context_pull.socket(zmq.PULL)

        ######SÓ PRA TESTAR EM CONEXÃO LOCAL SEM VM######
        try:
            self.pull_address = "tcp://localhost:5558"
            self.socket_resp.bind(self.pull_address)
        except zmq.error.ZMQError as e:
            self.pull_address = "tcp://localhost:5559"
            self.socket_resp.bind(self.pull_address)
        #################################################

        self.register()

        topic = "new_users" 
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic) #só se registra no tópico de novos usuários depois de se registrar para não ser notificado sobre a própria inscrição

    def register(self, flag=0, escolhas_topico = ""):
        if flag == 0: #caso "username inv" ele pode só tentar se registrar de novo sem selecionar "login ou novo usuário?" novamente
            login = input("Login (1)\nNovo usuário (2)\n ->")
        else:
            login = 2

        name = input("Login: ")
        password = input("Senha: ")
        if login == 1:
            message_regist = f"login {name} {password} {self.pull_address}" #mensagem pro servidor com login e senha para ver se já é um usuário registrado formato [operação] [dado dado dado... dado]. trata mensagem no server
            self.socket_resp.send_string(message_regist) #manda pro servidor
            resposta = self.socket_resp.recv_string() #analisa resposta
            if resposta == "liberado": #se já existe e senha correta
                print(f"Bem vindo de volta, {name}")
            elif resposta == "err_senha":
                print("Senha errada. Registre um novo usuário ou tente outra senha")
                self.register()
        else: #caso contrário
            if escolhas_topico == "":
                interesses = input("Digite tópicos de interesse (1 palavra por tópico): ")
                interesses = interesses.split(" ")
                interesses_str = ""
                for topico in interesses:
                    self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, topico)
                    interesses_str+=f"{topico} "
            else:
                interesses_str = escolhas_topico

            message_regist = f"register {name} {password} {self.pull_address} {interesses_str}"
            print(message_regist)
            self.socket_resp.send_string(message_regist) #manda pro servidor
            resposta = self.socket_resp.recv_string() #analisa resposta
            print(resposta)
            if resposta=="username inv":
                print(f"username invalido. {name} já existe.")
                self.register(1,interesses_str)
            else:
                print(f"Novo usuário registrado. Bem vindo, {name} !")


def register(socket_resp, socket_sub, pull_address, flag=0, escolhas_topico = ""):
        if flag == 0: #caso "username inv" ele pode só tentar se registrar de novo sem selecionar "login ou novo usuário?" novamente
            login = input("Login (1)\nNovo usuário (2)\n ->")
        else:
            login = 2

        name = input("Login: ")
        password = input("Senha: ")
        if login == 1:
            message_regist = f"login {name} {password} {pull_address}" #mensagem pro servidor com login e senha para ver se já é um usuário registrado formato [operação] [dado dado dado... dado]. trata mensagem no server
            socket_resp.send_string(message_regist) #manda pro servidor
            resposta = socket_resp.recv_string() #analisa resposta
            if resposta == "liberado": #se já existe e senha correta
                print(f"Bem vindo de volta, {name}")
            elif resposta == "err_senha":
                print("Senha errada. Registre um novo usuário ou tente outra senha")
                register(socket_resp,socket_sub,pull_address)
        else: #caso contrário
            if escolhas_topico == "":
                interesses = input("Digite tópicos de interesse (1 palavra por tópico): ")
                interesses = interesses.split(" ")
                interesses_str = ""
                for topico in interesses:
                    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topico)
                    interesses_str+=f"{topico} "
            else:
                interesses_str = escolhas_topico

            message_regist = f"register {name} {password} {pull_address} {interesses_str}"
            print(message_regist)
            socket_resp.send_string(message_regist) #manda pro servidor
            resposta = socket_resp.recv_string() #analisa resposta
            print(resposta)
            if resposta=="username inv":
                print(f"username invalido. {name} já existe.")
                register(socket_resp,socket_sub,pull_address,1,interesses_str)
            else:
                print(f"Novo usuário registrado. Bem vindo, {name} !")


def send_message(user_destino,socket_resp):
    message = f"request_info {user_destino}"
    socket_resp.send_string(message)



def client():
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    socket_sub.connect("tcp://localhost:5556")
    
    context_resp = zmq.Context()
    socket_resp = context_resp.socket(zmq.REQ)
    socket_resp.connect("tcp://localhost:5557")  # Assuming server is listening on port 5557
    #socket_resp.send_string(f"Received registration confirmation for client {client_id}")

    context_push = zmq.Context()
    socket_push = context_push.socket(zmq.PUSH)
    #ele faz a conexão pra enviar a mensagem conforme definido o destinatário então da pra deixar sem conexão por enquanto

    context_pull = zmq.Context()
    socket_pull = context_pull.socket(zmq.PULL)

    ######SÓ PRA TESTAR EM CONEXÃO LOCAL SEM VM######
    try:
        connection = "tcp://localhost:5558"
        socket_resp.bind(connection)
    except zmq.error.ZMQError as e:
        connection = "tcp://localhost:5559"
        socket_resp.bind(connection)
    #################################################

    print(connection)
    register(socket_resp, socket_sub, connection)

    topic = "new_users" 
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic) #só se registra no tópico de novos usuários depois de se registrar para não ser notificado sobre a própria inscrição

    

    #while True:
       # message = socket.recv_string()
        #topic, update = message.split()
        #print(f"Received {topic} {update}")


if __name__ == "__main__":
    C = Client()
