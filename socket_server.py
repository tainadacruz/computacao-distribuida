import zmq


class Server:
    def __init__(self):
        #Sockect publisher
        self.context_pub = zmq.Context()
        self.socket_pub = self.context_pub.socket(zmq.PUB)
        self.socket_pub.bind("tcp://*:5556")

        #Socket consumer
        self.context_con = zmq.Context()
        self.socket_con = self.context_con.socket(zmq.PULL)
        self.socket_con.bind("tcp://*:5557")

        self.run()

    def run(self):
        while True:
            message = self.socket_con.recv_string()
            if message:
                parse = message.split(" ")
                print(parse)
                op_code = parse[0]
                if op_code == ";;":
                    user = parse[1]
                    del parse[0:2]
                    send = " ".join(parse)
                    print(user)
                    print(send)
                    self.socket_pub.send_string(f"@{user}@ {send}")



if __name__ == "__main__":
    server_online = Server()
