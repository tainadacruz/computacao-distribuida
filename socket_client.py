import zmq
import os
import select
import sys

from configs import *
from sender import Sender
from user import User

class Client:
    def __init__(self):
        self.context_sub = zmq.Context()
        self.socket_sub = self.context_sub.socket(zmq.SUB)
        self.socket_sub.connect(TCP_IP_SUB_URL)
        
        self.context_resp = zmq.Context()
        self.socket_resp = self.context_resp.socket(zmq.REQ)
        self.socket_resp.connect(TCP_IP_RES_URL)
        
        #socket_resp.send_ýobj(f"Received registration confirmation for client {client_id}")
        
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

        self.user = None

        self.init()
        self.contatos = {} # Sockets de usuários amigos online (Colocar na classe User)
        topic = "new_users" 
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic) #só se registra no tópico de novos usuários depois de se registrar para não ser notificado sobre a própria inscrição
        self.run()


    def init(self, flag = 0, escolhas_topico = ""):
        if flag == 0: # Caso "username inv" ele pode só tentar se registrar de novo sem selecionar "login ou novo usuário"
            login = input("(1) Login\n(2) Novo usuário\n ->")
        else:
            login = 2

        name = input("Login: ")
        password = input("Senha: ")
                
        if login == "1":
            self.user = User(name, password, self.pull_address)
            self.login(self.user)
        else:
            self.user = User(name, password, self.pull_address)
            self.register(self.user, escolhas_topico)
            
                 
    def login(self, user):
        self.user.set_online(True)
        # self.user.set_socket(self.socket_pull)       SE DESCOMENTAR, QUEBRA TUDO
        
        self.socket_resp.send_pyobj(Sender('login', self.user)) # Manda pro servidor
        resposta = self.socket_resp.recv_pyobj() # Analisa resposta
            
        if resposta == "liberado": # Se já existe e senha correta
            print(f"Bem vindo de volta, {user.username}")
        elif resposta == "err_senha":
            print("Senha errada. Registre um novo usuário ou tente outra senha")
            self.init()
        
        
    def register(self, user, escolhas_topico):
        interesses_str = self.define_interests(escolhas_topico)

        self.user.interests = interesses_str
        self.user.set_online(True)
        # self.user.set_socket(self.socket_pull)       SE DESCOMENTAR, QUEBRA TUDO
        
        self.socket_resp.send_pyobj(Sender('register', self.user))  # Manda pro servidor
        resposta = self.socket_resp.recv_pyobj() # Analisa resposta
        print(resposta)
            
        if resposta=="username inv":
            print(f"Username inválido. {self.user.username} já existe.")
            self.init(1,interesses_str)
        else:
            USERS_DIC[self.user.username] = self.user.password
            USERS_OBJ.append(self.user)
            print(f"Novo usuário registrado. Bem vindo, {self.user.username} !")
            
            
    def define_interests(self, escolhas_topico):
        if escolhas_topico == "":
            interesses = input("Digite tópicos de interesse (1 palavra por tópico): ")
            interesses = interesses.split(" ")
            interesses_str = ""
            for topico in interesses:
                self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, topico)
                interesses_str+=f"{topico} "
        else:
            interesses_str = escolhas_topico
            
        return interesses_str
        

    def connect_target(self, user_destino):
        self.socket_resp.send_pyobj(Sender('request_info', user_destino))
        resposta = self.socket_resp.recv_pyobj()
        
        if resposta == "username not found" or resposta=="user offline":
            return resposta
        else:
            #message = input(f"Mensagem para {user_destino}: ")
            self.socket_push.connect(resposta)
            return resposta
            #self.socket_push.send_pyobj(message)
            #self.socket_push.disconnect(resposta)
            

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        estado_enviar_msg = False
        
        print(SEPARATOR)
        print("Para enviar uma mensagem para outro usuário digite @username_alvo")
        print("Para desconectar, digite logoff")
                
        fila = []
        while True:
            #os.system('cls' if os.name == 'nt' else 'clear')
            rlist, _, _ = select.select([sys.stdin,  self.socket_sub, self.socket_pull,], [], [])
            
            for ready in rlist:
                if ready == sys.stdin:
                    
                    if estado_enviar_msg:
                        user_input = sys.stdin.readline()
                        user_input = user_input.replace('\n',"")
                        user_input = f"@{self.name}:"+ user_input
                        
                        ###### TENTATIVAS:
                        
                        self.user.socket = self.socket_push
                        self.user.send_message(user_input)
                        self.socket_push.disconnect(resposta)
                        
                        print(f"{Color.YELLOW} mensagem enviada {Color.RESET}")
                        estado_enviar_msg = False
                    else:
                        user_input = sys.stdin.readline()
                        user_input = user_input.replace('\n',"")
                        
                        if user_input == "logoff": #OPÇÃO DESLOGAR
                            
                            
                            self.socket_resp.send_pyobj(Sender('logoff', self.user.username))
                            self.socket_resp.recv_pyobj()
                            quit()
                            
                        # DAQUI PRA BAIXO VAI QUEBRAR PORQUE NÃO CONSEGUI TESTAR:
                        
                        else: # OPÇÃO MANDAR MENSAGEM PRA USUÁRIO ALVO
                            user_alvo = user_input[1:]
                            if user_alvo not in self.contatos:
                                resposta = self.connect_target(user_alvo)
                                if resposta!="username not found" and resposta!="user offline":
                                    estado_enviar_msg = True
                                    print(f"{Color.YELLOW} digite a mensagem para {user_alvo} {Color.RESET}")
                                elif resposta == "username not found":
                                    print(resposta)
                                elif resposta == "user offline":
                                    # Se inscreve no tópico com nome do usuário alvo para ser notificado quando o usuário ficar online e offline para atualizar a lista de contatos local
                                    self.socket_sub.setsockopt_string(zmq.SUBSCRIBE,user_alvo)
                                    print(f"{resposta} você será notificado quando {user_alvo} ficar online")
                                #else:
                                    
                            user_input=""
                else:
                    try: # Receber mensagem de outros usuários pelo socket_pull assincronamente
                        message_received = self.socket_pull.recv_pyobj(flags=zmq.NOBLOCK)
                        fila.append(f"{Color.RED} {message_received} {Color.RESET}")
                        print(f"{Color.RED} {message_received} {Color.RESET}")

                    except :
                        pass
                    try: # Receber mensagem de quando um usuário de interesse ficou online/offline
                        message_received = self.socket_sub.recv_pyobj(flags=zmq.NOBLOCK)
                        fila.append(f"{Color.GREEN} **server: {message_received} ** {Color.RESET}")
                        print(F"{Color.GREEN} **server: {message_received} ** {Color.RESET}" )
                    except:
                        pass

    #while True:
       # message = socket.recv_pyobj()
        #topic, update = message.split()
        #print(f"Received {topic} {update}")


if __name__ == "__main__":
    C = Client()
