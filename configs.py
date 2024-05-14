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
    
PORT_5556 = f'5556'
PORT_5557 = f'5557'
    
TCP_IP_SUB_URL = f'tcp://localhost:{PORT_5556}'
TCP_IP_REQ_URL = f'tcp://localhost:{PORT_5557}'

SOCKETS = ["tcp://localhost:5558",
           "tcp://localhost:5559",
           "tcp://localhost:5560",
           "tcp://localhost:5561",
           "tcp://localhost:5562",
           "tcp://localhost:5563"]


USERS_OBJ = []
USERS_DIC = {'A': '123', 'B': '123'}

SEPARATOR = "------------------------------------------"

OK = f''

def instructions():
    print(SEPARATOR)
    print("Para enviar um email para outro usuário digite @username_alvo ou @tópico_alvo")
    print("Para iniciar uma conversa com outro usuário digite #username_alvo")
    print("Para ver novas mensagens, digite refresh")
    print("Para se inscrever em um tópico, digite !tópico")
    print("Para desconectar, digite logoff")


