import zmq

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
        #Inscreve no socket publisher do servidor
        self.context_sub = zmq.Context()
        self.socket_sub = self.context_sub.socket(zmq.SUB)
        self.socket_sub.connect("tcp://localhost:5556")

        #Conecta ao socket pull do servidor
        self.context_push = zmq.Context()
        self.socket_push = self.context_push.socket(zmq.PUSH)
        self.socket_push.connect("tcp://localhost:5557")

        #Executa
        self.register()
        self.run()

    def register(self):
        while True:
            name = input("Insira seu email\n->")
            confirm = input(f"O email {name} está correto?(Y/N)\n->")
            if confirm == "Y":
                break
        self.name = name
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, self.name)

    def run(self):
        estado_enviar_msg = False
        print("Começar Loop")
        print("Para enviar uma mensagem para outro usuário digite @username_alvo")
        print("Para ver novas mensagens digite refresh")
        print("Para se inscrever a um tópico digite !nome_tópico")
        print("Para desconectar digite logoff")
        user_alvo = None
        while True:
            if not estado_enviar_msg:
                user_input = input("->")
            if estado_enviar_msg:
                user_input = input("Escreva sua mensagem:\n")
                self.socket_push.send_string(f";;{user_alvo};;\nDe: {self.name}\n{user_input}")
                print(f"{Color.YELLOW} mensagem enviada {Color.RESET}")
                user_alvo = None
                estado_enviar_msg = False
            else:
                if user_input=="logoff": #OPÇÃO DESLOGAR
                    quit()
                elif user_input=="refresh": #OPÇÃO RECEBER NOVAS MENSAGENS
                    self.socket_push.send_string(f"refresh {self.socket_sub.getsockopt_string()}")
                    while True:
                        try:
                            message_received = self.socket_sub.recv_string(flags=zmq.NOBLOCK)
                            print(f"{Color.RED} {message_received} {Color.RESET}")
                            print("\n")
                        except:
                            print("Mensagens Recebidas")
                            break
                elif user_input[0] == "!": #OPÇÃO SE INSCREVER A UM TÓPICO
                    topic = user_input[1:]
                    self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic)
                    print(self.socket_sub.getsockopt_string(zmq.SUBSCRIBE))
                elif user_input[0] == "@": #OPÇÃO MANDAR MENSAGEM PRA USUÁRIO ALVO
                    user_alvo = user_input[1:]
                    estado_enviar_msg = True
                else:
                    print("Comando não reconhecido")


if __name__ == "__main__":
    C = Client()
