import socket
import queue

def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is listening...")

    response_queue = queue.Queue()

    while True:
        conn, address = server_socket.accept()
        print("Connected to client: ", address)

        try:
            data = conn.recv(1024).decode()
            if not data:
                print("Client {} disconnected.".format(address))
                break
            
            response_queue.put((conn, address, data))
        except ConnectionResetError:
            print("Client {} disconnected.".format(address))
            break

        if not response_queue.empty():
            conn, address, response_atual = response_queue.get()
            print("Received from client {}: {}".format(address, data))
            response = input('Response to client {}: '.format(address))
            conn.send(response.encode())

        conn.close()

if __name__ == '__main__':
    server_program()
