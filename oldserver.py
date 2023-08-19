#server side code
import socket
import threading
import sys

#getting ip ad port and header
HEADER = 1024
FORMAT = 'utf-8'

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #gets the ip address of the server

#picking the socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
ADDR = (SERVER, PORT)

#binding the socket to the server
server.bind(ADDR)







#function to handle the clients
def handle_client(con, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = con.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break  # Client disconnected

            msg_length = int(msg_length)
            msg = con.recv(msg_length).decode(FORMAT)
            
            if msg == "turn on":
                 device_state = "on".encode(FORMAT)
                 print(f"[{addr}] Device is now ON")

            elif msg == "turn off":
                device_state = "off".encode(FORMAT)
                print(f"[{addr}] Device is now OFF")

            elif msg == "quit":
                print(f"[{addr}] Client is quitting...")
                break
             

            else:
                print(f"[{addr}] Unknown command: {msg}")

            con.send(("Device state is now: " + device_state.decode(FORMAT)).encode(FORMAT)) # sending a msg to the client



        except ConnectionResetError:
            print(f"[{addr}] Client connection reset.")
            break


    print(f"[{addr}] Connection closed.")
    con.close()












#function to start the serverf start():
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        con, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (con, addr)) #creating a thread for each client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        if threading.activeCount() == 1:
            print("[SERVER] Server is shutting down...")
            server.close()
            sys.exit()



print ("[STARTING] server is starting...")
start()
