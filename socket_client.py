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
        #Inscreve no socket publisher do servidor
        self.context_sub = zmq.Context()
        self.socket_sub = self.context_sub.socket(zmq.SUB)
        self.socket_sub.connect("tcp://localhost:5556")

        #Conecta ao socket rep do servidor
        self.context_req = zmq.Context()
        self.socket_req = self.context_req.socket(zmq.REQ)
        self.socket_req.connect("tcp://localhost:5557")

        #Cria mas não conecta socket para enviar mensagens
        self.context_enviar = zmq.Context()
        self.socket_enviar = self.context_enviar.socket(zmq.PUSH)

        #Cria mas não conecta socket para receber mensagens
        self.context_receber = zmq.Context()
        self.socket_receber = self.context_receber.socket(zmq.PULL)

        #Executa
        self.register()
        self.run()

    def register(self):
        while True:
            name = input("Insira seu email\n->")
            confirm = input(f"O email {name} está correto?(Y/N)\n->")
            if confirm == "Y" or confirm == "y":
                break
        self.name = name
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, f"@{self.name}@")
        print(f"Quais seus interesses?")
        while True:
            interesse = input("->")
            self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, f"@{interesse}@")
            accept = input("Algo mais? (Y/N)\n->")
            if accept == "N" or accept == "n":
                break
            print("Digite mais um interesse")
        self.socket_req.send_string(f"reg {name}")
        resposta = self.socket_req.recv_string()
        resposta = resposta.split(" ")
        #self.address_enviar = resposta[0]
        self.address_receber = resposta[1]
        print(resposta)
        #self.socket_enviar.connect(self.address_enviar)
        self.socket_receber.bind(self.address_receber)
       # self.socket_enviar.send_string("teste")
       # msg = self.socket_receber.recv_string()
       # print(msg)



    def run(self):
        estado_enviar_msg = False
        estado_receber_msg = False
        novas_mensagems = False
        reprint = False
        estado_aguardando_conversa = False
        estado_aceitando_conversado = False
        print("Começar Loop")
        print("Para enviar um email para outro usuário digite @username_alvo ou @tópico_alvo")
        print("Para iniciar uma conversa com outro usuário digite #username_alvo")
        print("Para ver novas mensagens digite refresh")
        print("Para se inscrever em um tópico digite !tópico")
        print("Para desconectar digite logoff")
        user_alvo = None
        while True:
            #print("AAAAAAAAAAAAAA")
            if novas_mensagems and reprint:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Começar Loop")
                print("Para enviar um email para outro usuário digite @username_alvo ou @tópico_alvo")
                print("Para iniciar uma conversa com outro usuário digite #username_alvo")
                print("Para ver novas mensagens digite refresh")
                print("Para se inscrever em um tópico digite !tópico")
                print("Para desconectar digite logoff")
                #if(novas_mensagems):
                #    print(f"{Color.GREEN} Novas mensagens no refresh {Color.RESET}")
                #    reprint = False
            rlist, _, _ = select.select([sys.stdin, self.socket_receber], [], [])
            for ready in rlist:
                if ready == sys.stdin:

                    user_input=sys.stdin.readline()
                    user_input = user_input.replace('\n',"")
                    if user_input=="logoff": #OPÇÃO DESLOGAR
                        quit()
                    elif user_input=="refresh": #OPÇÃO RECEBER NOVAS MENSAGENS
                        while True:
                            try:
                                message_received = self.socket_sub.recv_string(flags=zmq.NOBLOCK)
                                correct = message_received.split(" ")
                                print(correct)
                                if correct[0] == f"@{self.name}@":
                                    del correct[0]
                                else:
                                    correct[0] = f"Tópico: {correct[0][1:(len(correct[0]) - 1)]}\n{correct[1]}"
                                    del correct[1]
                                print(correct)
                                if correct[0] == "pedido_conversa":
                                    #self.socket_pub.send_string(f"@{nome_alvo}@ pedido_conversa {nome_pedindo} {socket_pedindo}")
                                    resposta = input(f"usuário {correct[1]} deseja conversar com você. Aceita? (Y/N)\n-> ")
                                    resposta = resposta.lower()
                                    if resposta == "y":
                                        self.temp_string = correct
                                        estado_receber_msg = True
                                        break
                                        
                                
                                #print(correct)
                                to_print = " ".join(correct)
                                print(f"{Color.RED}{to_print}{Color.RESET}")
                                print("\n")
                            except:
                                print("Mensagens Recebidas")
                                novas_mensagems = False
                                break
                    elif user_input[0] == "@": #OPÇÃO MANDAR MENSAGEM PRA USUÁRIO ALVO
                        user_alvo = user_input[1:]
                        user_input = input("Escreva sua mensagem:\n")
                        self.socket_req.send_string(f";; {user_alvo} De: {self.name}\n{user_input}")
                        self.socket_req.recv_string()
                        print(f"{Color.YELLOW} mensagem enviada {Color.RESET}")
                        user_alvo = None
                        estado_enviar_msg = False
                    elif user_input[0] == "!": #OPÇÃO INSCREVER EM UM TÓPICO
                        topic = user_input[1:]
                        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, f"@{topic}@")
                    elif user_input[0] == "#":
                        user_alvo = user_input[1:]
                        print(user_alvo)
                        self.socket_req.send_string(f"# {self.name} {user_alvo} {self.address_receber}")
                        resposta = self.socket_req.recv_string()
                        estado_aguardando_conversa = True
    
                    else:
                        print("Comando não reconhecido")

                    if estado_receber_msg:
                        print("Enviando")
                        print(self.temp_string)
                        self.socket_enviar.connect(self.temp_string[2])
                        print(self.address_receber)
                        self.socket_enviar.send_string(f"{self.address_receber}")
                        print("Enviado")
                        #self.socket_enviar.recv_string()
                        print("respondido")
                        estado_receber_msg = False
                        estado_aceitando_conversado = True
                        break

               # elif ready == self.socket_sub:
                #    try: #Receber mensagem de quando um usuário de interesse ficou online/offline
                 #       message_received = self.socket_sub.recv_string(flags=zmq.NOBLOCK)
                  #      fila.append(f"{Color.GREEN} **server: {message_received} ** {Color.RESET}")
                   #     print(F"{Color.GREEN} **server: {message_received} ** {Color.RESET}" )
                   # except:
                   #     pass


                elif ready == self.socket_receber and (estado_aguardando_conversa or estado_aceitando_conversado):
                    if estado_aguardando_conversa:
                        print("estou aqui")
                        endereço = self.socket_receber.recv_string()
                        print(endereço)
                        self.socket_enviar.connect(endereço)
                       # self.socket_receber.send_string("")#ack

                    loop = True
                    #user_input = ""

                    print("INICIANDO CONVERSA (digite 'quit' para voltar ao menu principal) \n -> ")
                    while loop:
                            rlist2, _, _ = select.select([sys.stdin, self.socket_receber], [], [])
                            for ready in rlist2:
                                
                                while True:
                                    try:
                                        msg = self.socket_receber.recv_string(flags = zmq.NOBLOCK)
                                       # self.socket_receber.send_string("")
                                        #print("ack")
                                        print(f"{msg}")
                                    except zmq.error.Again:
                                        break

                                if ready == sys.stdin:
                                    user_input= sys.stdin.readline()
                                    user_input = user_input.replace('\n',"")
                                    if user_input=="quit":
                                        self.socket_enviar.send_string(f"{self.name}: *desconectou*")
                                        print("*DESCONECTANDO DA CONVERSA*")
                                        loop = False
                                    else:
                                        self.socket_enviar.send_string(f"{self.name}: {user_input}")
                    




if __name__ == "__main__":
    C = Client()
