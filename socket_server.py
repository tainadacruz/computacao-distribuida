import zmq
import time


class Server:
    def __init__(self):
        self.context_pub = zmq.Context()
        self.socket_pub = self.context_pub.socket(zmq.PUB) #cria o socket de publisher para anunciar usuários novos com interesses similares
        self.socket_pub.bind("tcp://*:5556")
        self.context_rep = zmq.Context()
        self.socket_rep = self.context_rep.socket(zmq.REP) #cria o socket de resposta a requisição para registros de usuário e pedidos de dados.
        self.socket_rep.bind("tcp://*:5557")
        self.users_senhas = {} #dicionário para usuário e senha
        self.users_sockets = {} #dicionário para usuário e socket (TODO: Descobrir como fazer o usuário mandar o socket para mensagens dele.) talvez mudar nome para users_online
        self.run()
        #self.//topic = "events"

    def login_users(self,parse):
        new_message = ""
        if parse[0] == "login": #message = "login user password pull_address"
            user = parse[1]
            password = parse[2]
            pull_address = parse[3]
            if user in self.users_senhas:
                if self.users_senhas[user] == password:
                    new_message = "liberado"
                    self.users_sockets[user] = pull_address #atualiza socket do usuário
                else:
                    new_message = "err_senha"
        elif parse[0] == "register": #message = register user password pull_address t0 t1 t2...
            print("registro")
            user = parse[1]
            if user in self.users_senhas:
                new_message = "username inv"
            else:
                password = parse[2]
                pull_address = parse[3]
                self.users_senhas[user] = password #registra senha
                self.users_sockets[user] = pull_address #registra socket
                new_message = "new_user"

        return new_message

    def run(self):
        while True:

            message = self.socket_rep.recv_string()
            if message:
                parse = message.split(" ")
                if parse[0] == "login" or parse[0] == "register":
                    new_message = self.login_users(parse)
                
                print(f"respota: {new_message}")
                self.socket_rep.send_string(new_message)



                #if new_message == "new_user": #isso seria pra anunciar pro mundo que tem um novo usuário, seria absolutamente insuportável em uma aplicação de verdade com 100000 usuários que cresce todo dia
                #    self.socket_pub.send_string(f"{new_message} {user}") #incluir depois {address} quando eu descobrir como mandar o socket de receber mensagem do usuário.

            print(self.users_senhas)
            print(self.users_sockets)

           # message = f"Update_{request}"

          #  print(f"Publishing {topic} {message}")

          # socket.send_string(f"{topic} {message}")


           # time.sleep(1)

def server():
    context_pub = zmq.Context()

    socket_pub = context_pub.socket(zmq.PUB) #cria o socket de publisher para anunciar usuários novos com interesses similares
    socket_pub.bind("tcp://*:5556")

    context_rep = zmq.Context()
    socket_rep = context_rep.socket(zmq.REP) #cria o socket de resposta a requisição para registros de usuário e pedidos de dados.
    socket_rep.bind("tcp://*:5557")

    users_senhas = {} #dicionário para usuário e senha
    users_sockets = {} #dicionário para usuário e socket (TODO: Descobrir como fazer o usuário mandar o socket para mensagens dele.) talvez mudar nome para users_online

    topic = "events"

    while True:

        message = socket_rep.recv_string()
        if message:
            new_message = ""
            parse = message.split(" ")
            if parse[0] == "login": #message = "login user password pull_address"
                user = parse[1]
                password = parse[2]
                pull_address = parse[3]
                if user in users_senhas:
                    if users_senhas[user] == password:
                        new_message = "liberado"
                        users_sockets[user] = pull_address #atualiza socket do usuário
                    else:
                        new_message = "err_senha"

            elif parse[0] == "register": #message = register user password pull_address t0 t1 t2...
                print("registro")
                user = parse[1]
                if user in users_senhas:
                    new_message = "username inv"
                else:
                    password = parse[2]
                    pull_address = parse[3]
                    users_senhas[user] = password #registra senha
                    users_sockets[user] = pull_address #registra socket
                    new_message = "new_user"
            
            print(f"respota: {new_message}")
            socket_rep.send_string(new_message)



            if new_message == "new_user": #isso seria pra anunciar pro mundo que tem um novo usuário, seria absolutamente insuportável em uma aplicação de verdade com 100000 usuários que cresce todo dia
                socket_pub.send_string(f"{new_message} {user}") #incluir depois {address} quando eu descobrir como mandar o socket de receber mensagem do usuário.

        print(users_senhas)
        print(users_sockets)

       # message = f"Update_{request}"

      #  print(f"Publishing {topic} {message}")

      # socket.send_string(f"{topic} {message}")


       # time.sleep(1)


if __name__ == "__main__":
    server_online = Server()
