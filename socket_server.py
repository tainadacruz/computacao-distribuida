import json
import zmq
import time

from configs import *
from user import User


class Server:
    def __init__(self):
        self.context_pub = zmq.Context()
        self.socket_pub = self.context_pub.socket(zmq.PUB) #cria o socket de publisher para anunciar usuários novos com interesses similares
        self.socket_pub.bind(f'tcp://*:{PORT_5556}')
        
        self.context_rep = zmq.Context()
        self.socket_rep = self.context_rep.socket(zmq.REP) #cria o socket de resposta a requisição para registros de usuário e pedidos de dados.
        self.socket_rep.bind(f'tcp://*:{PORT_5557}')
        
        self.users_sockets = {} # Usando SOCKETS no lugar (TODO: Descobrir como fazer o usuário mandar o socket para mensagens dele.) talvez mudar nome para users_online
        self.run()
        #self.//topic = "events"

    def init_users(self, op_code, user):
        new_message = ""
                
        if op_code == "login": # message = "login user"
            if user.username in USERS_DIC:
                if USERS_DIC[user.username] == user.password:
                    new_message = "liberado"
                else:
                    new_message = "err_senha"
                    
        elif op_code == "register": # message = register user...
            if user.username in USERS_DIC:
                new_message = "username inv"
            else:
                USERS_DIC[user.username] = user.password # Registra senha
                SOCKETS[user.username] = user.socket #registra socket
                new_message = "new_user"

        return new_message

    def provide_socket(self, username):
        if username in SOCKETS:
            new_message = SOCKETS[username]
            print(new_message)
        else:
            if username in USERS_DIC: #Se não está na lista de sockets (deleta o item quando o usuário desloga) mas está na lista de usuários, ele está offline
                new_message = "user offline"
            else:
                new_message = "username not found"

        return new_message

    def run(self):
        while True:
            reiceved = self.socket_rep.recv_pyobj()
            op_code = reiceved.flag
            user = reiceved.object
                        
            if op_code:
                if op_code == "login" or op_code == "register":
                    new_message = self.init_users(op_code, user)
                    #print(f"{user} connected {user.pull_address}")
                    self.socket_pub.send_pyobj(f"{user.username} connected {user.pull_address}")
                    
                if op_code == "request_info":
                    new_message = self.provide_socket(user)
                    
                elif op_code == "logoff":
                    del SOCKETS[user]
                    new_message = "logged off"
                    print(f"{user.username} disconnected")
                    self.socket_pub.send_pyobj(f"{user.username} disconnected")
                
               # print(f"respota: {new_message}")
                self.socket_rep.send_pyobj(new_message)

                #if new_message == "new_user": #isso seria pra anunciar pro mundo que tem um novo usuário, seria absolutamente insuportável em uma aplicação de verdade com 100000 usuários que cresce todo dia
                #    self.socket_pub.send_pyobj(f"{new_message} {user}") #incluir depois {address} quando eu descobrir como mandar o socket de receber mensagem do usuário.

            #print(self.users_senhas)
            #print(self.users_sockets)

           # message = f"Update_{request}"

          #  print(f"Publishing {topic} {message}")

          # socket.send_pyobj(f"{topic} {message}")


           # time.sleep(1)


if __name__ == "__main__":
    server_online = Server()
