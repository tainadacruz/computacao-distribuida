import zmq

from configs import *
from package import Package


class Server:
    def __init__(self):
        # Socket Publisher
        self.context_pub = zmq.Context()
        self.socket_pub = self.context_pub.socket(zmq.PUB)
        self.socket_pub.bind(f'tcp://*:{PORT_5556}')

        # Socket Consumer
        self.context_con = zmq.Context()
        self.socket_con = self.context_con.socket(zmq.REP)
        self.socket_con.bind(F'tcp://*:{PORT_5557}')

        self.fila_sockets = SOCKETS
        self.users = {}

        self.run()

    def run(self):
        while True:
            message = self.socket_con.recv_pyobj()
            op_code = message.flag
            obj = message.object.split(' ')
            
            if message:
                if op_code == ";;":
                    self.socket_con.send_pyobj(Package('', OK))
                    user = obj[0]
                    del obj[0]
                    send = ' '.join(obj)
                    print(user)
                    print(send)
                    self.socket_pub.send_pyobj(Package('', f"@{user}@ {send}"))
                elif op_code == "reg": # Registro
                    name = obj[0]
                    socket_emprestado_enviar = self.fila_sockets.pop()
                    socket_emprestado_receber = self.fila_sockets.pop()
                    self.socket_con.send_pyobj(Package('', f'{socket_emprestado_enviar} {socket_emprestado_receber}'))
                    self.users[name] = socket_emprestado_receber
                elif op_code == "#": # Iniciar conversa privada
                    nome_pedindo = obj[0]
                    nome_alvo = obj[1]
                    socket_pedindo = obj[2]
                    self.socket_pub.send_pyobj(Package('', f'@{nome_alvo}@ pedido_conversa {nome_pedindo} {socket_pedindo}'))
                    self.socket_con.send_pyobj(Package('', OK)) # Pedido enviado


if __name__ == "__main__":
    server_online = Server()
