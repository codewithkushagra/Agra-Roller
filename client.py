import socket
import break_msg

port=5050  #server port used
header=64
Format="utf-8"
start_bit="78 78"
packet_lenght="0D"
protocal_number="01"
disconnect_msg="!DISCONNECT"
Server="0.0.0.0"
Addr=(Server, port)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(Addr)

def send(msg):
    message=msg  #encode the string in the bit format
    client.send(message)
    m=break_msg.breaker(msg)
    if m[2]=="01":
        print(client.recv(1024).decode(Format))
    
send("Hi")


