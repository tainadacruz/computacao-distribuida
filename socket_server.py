import zmq

from configs import *


class Server:
    def __init__(self):
        #Sockect publisher
        self.context_pub = zmq.Context()
        self.socket_pub = self.context_pub.socket(zmq.PUB)
        self.socket_pub.bind(f'tcp://*:{PORT_5556}')

        #Socket consumer
        self.context_con = zmq.Context()
        self.socket_con = self.context_con.socket(zmq.REP)
        self.socket_con.bind(F'tcp://*:{PORT_5557}')

        self.fila_sockets = ["tcp://localhost:5558","tcp://localhost:5559","tcp://localhost:5560","tcp://localhost:5561","tcp://localhost:5562","tcp://localhost:5563"]

        self.users = {}

        self.run()

    def run(self):
        while True:
            message = self.socket_con.recv_pyobj()
            print(message)
            if message:
                parse = message.split(" ")
                print(parse)
                op_code = parse[0]
                if op_code == ";;":
                    self.socket_con.send_pyobj(ACK)
                    user = parse[1]
                    del parse[0:2]
                    send = " ".join(parse)
                    print(user)
                    print(send)
                    self.socket_pub.send_pyobj(f"@{user}@ {send}")
                elif op_code == "reg": #registro
                    name = parse[1]
                    socket_emprestado_enviar = self.fila_sockets.pop()
                    socket_emprestado_receber = self.fila_sockets.pop()
                    self.socket_con.send_pyobj(f"{socket_emprestado_enviar} {socket_emprestado_receber}")
                    self.users[name] = socket_emprestado_receber
                elif op_code == "#": #iniciar conversa privada
                    nome_pedindo = parse[1]
                    nome_alvo = parse[2]
                    socket_pedindo = parse[3]
                    self.socket_pub.send_pyobj(f"@{nome_alvo}@ pedido_conversa {nome_pedindo} {socket_pedindo}")
                    self.socket_con.send_pyobj(ACK) #ack. pedido enviado




if __name__ == "__main__":
    server_online = Server()
