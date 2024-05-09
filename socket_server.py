import zmq
import time


def publisher():
    context_pub = zmq.Context()

    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.bind("tcp://*:5556")

    context_rep = zmq.Context()
    socket_rep = context_rep.socket(zmq.REP)
    socket_rep.bind("tcp://*:5557")

    users_senhas = {}
    users_sockets = {}

    topic = "events"

    while True:

        message = socket_rep.recv_string()
        if message:
            parse = message.split(" ")
            if parse[0] == "check_register":
                _,user,password = parse
                if user in users_senhas:
                    if users_senhas[user] == password:
                        new_message = "liberado"
                    else:
                        new_message = "err_senha"
                else:
                    users_senhas[user] = password
                    new_message = "new_user"

            socket_rep.send_string(new_message)

            if new_message == "new_user": #isso seria pra anunciar pro mundo que tem um novo usuário, seria absolutamente insuportável em uma aplicação de verdade com 100000 usuários que cresce todo dia
                socket_pub.send_string(f"{new_message} {name}") #incluir depois {address} quando eu descobrir como mandar o socket de receber mensagem do usuário.

        print(users_senhas)

       # message = f"Update_{request}"

      #  print(f"Publishing {topic} {message}")

      # socket.send_string(f"{topic} {message}")


       # time.sleep(1)


if __name__ == "__main__":
    publisher()
