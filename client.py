import socket
import time


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect(ADDR)

#funtion to send a msg to the server
def send(msg):
    """Sends a message to the server."""
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght)) #adding spaces to the msg lenght to make it 64 bytes
    client.send(send_lenght)
    client.send(message)
    print(client.recv(2048).decode(FORMAT)) #printing the msg received from the server


device_on_time = 0 #time the device was turned on
device_is_on = False #initially the device is off


def get_user_input():
    """Gets the user's input."""
    user_input = input("Do you want to turn on or turn off the device? ")
    return user_input


while True:
    user_input = get_user_input()

    if user_input == "on":
        if device_is_on:
            print("Device is already on.")
        else:
            send("turn on")
            device_on_time = time.time()
            device_is_on = True
    elif user_input == "off":
        if device_is_on:
            send("turn off")
            print("Device was turned ON for: " + str(time.time() - device_on_time))
            device_is_on = False
        else:
            print("Device is already off.")
    elif user_input == "quit":
        break
    else:
        print("Invalid input.")

send("quit") #sending a msg to the server to close the connection
