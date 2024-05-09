import zmq

def register(socket_resp):
        name = input("Login: ")
        password = input("Senha: ")

        message_regist = f"check_register {name} {password}" #mensagem pro servidor com login e senha para ver se já é um usuário registrado formato [operação] [dado dado dado... dado]. trata mensagem no server
        socket_resp.send_string(message_regist) #manda pro servidor
        resposta = socket_resp.recv_string() #analisa resposta
        if resposta == "liberado": #se já existe e senha correta
            print(f"Bem vindo de volta, {name}")
        elif resposta == "err_senha":
            print("Senha errada. Registre um novo usuário ou tente outra senha")
            register(socket_resp)
        else: #caso contrár
            print(f"Novo usuário registrado. Bem vindo, {name} !")

def subscriber():
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    socket_sub.connect("tcp://localhost:5556")
    
    context_resp = zmq.Context()
    socket_resp = context_resp.socket(zmq.REQ)
    socket_resp.connect("tcp://localhost:5557")  # Assuming server is listening on port 5557
    #socket_resp.send_string(f"Received registration confirmation for client {client_id}")

    register(socket_resp)

    topic = "new_users"
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic)

    

    #while True:
       # message = socket.recv_string()
        #topic, update = message.split()
        #print(f"Received {topic} {update}")


if __name__ == "__main__":
    subscriber()
