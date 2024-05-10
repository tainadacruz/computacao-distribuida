import zmq
import os
import select
import sys

class Color:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'

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
        #self.socket_pull.setsockopt(zmq.RCVTIMEO, 10)

        ######SÓ PRA TESTAR EM CONEXÃO LOCAL SEM VM######
        try:
            self.pull_address = "tcp://localhost:5558"
            self.socket_pull.bind(self.pull_address)
        except zmq.error.ZMQError as e:
            self.pull_address = "tcp://localhost:5559"
            self.socket_pull.bind(self.pull_address)
        #################################################

        self.register()
        self.contatos = {} #sockets de usuários amigos online
        topic = "new_users" 
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic) #só se registra no tópico de novos usuários depois de se registrar para não ser notificado sobre a própria inscrição
        self.run()

    def register(self, flag=0, escolhas_topico = ""):
        if flag == 0: #caso "username inv" ele pode só tentar se registrar de novo sem selecionar "login ou novo usuário?" novamente
            login = input("Login (1)\nNovo usuário (2)\n ->")
        else:
            login = 2

        name = input("Login: ")
        password = input("Senha: ")
        self.name = name
        if login == "1":
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



    def connect_target(self, user_destino):
        message = f"request_info {user_destino}"
       # print(message)
        self.socket_resp.send_string(message)
        resposta = self.socket_resp.recv_string()
        if resposta == "username not found" or resposta=="user offline":
            return resposta
        else:
            #message = input(f"Mensagem para {user_destino}: ")
            self.socket_push.connect(resposta)
            return resposta
            #self.socket_push.send_string(message)
            #self.socket_push.disconnect(resposta)

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        estado_enviar_msg = False
        print("Começar Loop")
        print("Para enviar uma mensagem para outro usuário digite @username_alvo")
        print("Para desconectar digite logoff")
        fila = []
        while True:
            #os.system('cls' if os.name == 'nt' else 'clear')
            rlist, _, _ = select.select([sys.stdin,  self.socket_sub, self.socket_pull,], [], [])
            for ready in rlist:
                if ready == sys.stdin:
                    if estado_enviar_msg:
                        user_input=sys.stdin.readline()
                        user_input = user_input.replace('\n',"")
                        user_input = f"@{self.name}:"+ user_input
                        self.socket_push.send_string(user_input)
                        self.socket_push.disconnect(resposta)
                        print(f"{Color.YELLOW} mensagem enviada {Color.RESET}")
                        estado_enviar_msg = False
                    else:
                        user_input=sys.stdin.readline()
                        user_input = user_input.replace('\n',"")
                        if user_input=="logoff": #OPÇÃO DESLOGAR
                            self.socket_resp.send_string(f"{user_input} {self.name}")
                            self.socket_resp.recv_string()
                            quit()
                        else: #OPÇÃO MANDAR MENSAGEM PRA USUÁRIO ALVO
                            user_alvo = user_input[1:]
                            if user_alvo not in self.contatos:
                                resposta = self.connect_target(user_alvo)
                                if resposta!="username not found" and resposta!="user offline":
                                    estado_enviar_msg = True
                                    print(f"{Color.YELLOW} digite a mensagem para {user_alvo} {Color.RESET}")
                                elif resposta == "username not found":
                                    print(resposta)
                                elif resposta == "user offline":
                                    #Se inscreve no tópico com nome do usuário alvo para ser notificado quando o usuário ficar online e offline para atualizar a lista de contatos local
                                    self.socket_sub.setsockopt_string(zmq.SUBSCRIBE,user_alvo)
                                    print(f"{resposta} você será notificado quando {user_alvo} ficar online")
                                #else:
                                    

                            user_input=""
                else:
                    try: #Receber mensagem de outros usuários pelo socket_pull assincronamente
                        message_received = self.socket_pull.recv_string(flags=zmq.NOBLOCK)
                        fila.append(f"{Color.RED} {message_received} {Color.RESET}")
                        print(f"{Color.RED} {message_received} {Color.RESET}")

                    except :
                        pass
                    try: #Receber mensagem de quando um usuário de interesse ficou online/offline
                        message_received = self.socket_sub.recv_string(flags=zmq.NOBLOCK)
                        fila.append(f"{Color.GREEN} **server: {message_received} ** {Color.RESET}")
                        print(F"{Color.GREEN} **server: {message_received} ** {Color.RESET}" )
                    except:
                        pass
                    
                    


    #while True:
       # message = socket.recv_string()
        #topic, update = message.split()
        #print(f"Received {topic} {update}")


if __name__ == "__main__":
    C = Client()
