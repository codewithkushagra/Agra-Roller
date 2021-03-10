import socket
import threading
import Data_Base
import libscrc
from datetime import datetime
port=5050  #server port used
header=64
disconnect_msg="!DISCONNECT"
Server="0.0.0.0"  #getting server name

Addr=(Server, port)  #addr of server 

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #defining type of socket
server.bind(Addr)  #binds the terminal to server socket

#crcx25 check
def crc_check(string_crc,error_check):
    crc16 = libscrc.x25(string_crc)
    var=0
    final_crc=""
    for j in hex(crc16):
        if var>1:
            final_crc=final_crc+j
        var+=1
    if len(final_crc)==3:
        final_crc="0"+final_crc
    elif len(final_crc)==2:
        final_crc="00"+final_crc
    elif len(final_crc)==1:
        final_crc="000"+final_crc
    print(f"Generated crc: {final_crc}")
    print(f"sent by terminal: {error_check}")
    if final_crc==error_check:
        return 1
    else:
        return 0
    
#handles the client request
#sno update left
def handle_client(conn, addr):
    print(f"New connection : [{addr}]")
    connected=True
    sno=0
    snoh=0
    snot=0
    terminal_id=""
    snoc=0
    login="login_not_done"
    while connected:
            #if login=="login_done":
            #    message=input("Enter the message you want to send: ")
            #    cpacket_length=len(message)+12
            #    cpl=hex(cpacket_length)
            #    mk=0
            #    ghj=""
            #    for i in cpl:
            #        if mk>1:
            #            ghj=ghj+i
            #        mk+=1
            #    if len(ghj)==1:
            #        ghj="0"+ghj
            #    command_len=hex(len(message)+4)
            #    jjk=""
            #    mk=0
            #    for j in command_len:
            #        if mk>1:
            #            jjk=jjk+j
            #        mk+=1
            #    if len(jjk)==1:
            #        jjk="0"+jjk
            #    enmessage=message.encode().hex()
            #    if snoc<65353:
            #            snoc+=1
            #    else:
            #            snoc=0
            #    uu=0
            #    ss=""
            #    snohmc=hex(snoc)
            #    for k in snohmc:
            #            if uu>1:
            #                ss=ss+k
            #            uu+=1
            #    if len(ss)==1:
            #            ss="000"+ss
            #    elif len(ss)==2:
            #            ss="00"+ss
            #    elif len(ss)==3:
            #            ss="0"+ss
            #    nu=0
            #    return_crc=""
            #    for cp in hex(libscrc.x25(bytes.fromhex(ghj+"80"+jjk+"0000"+enmessage+"0002"+ss))):
            #                 if nu>1:
            #                   return_crc=return_crc+cp
            #                 nu+=1
            #    if len(return_crc)==3:
            #                   return_crc="0"+return_crc

            #    command="7878"+ghj+"80"+jjk+"0000"+enmessage+"0002"+ss+return_crc+"0d0a"
            #    command=bytes.fromhex(command)
            #    conn.send(command)
            #    return_crc=""



                #command="787810800900004487888823000200011dab0d0a"
                #scommand=bytes.fromhex(command)
                #print(scommand)
                #conn.send(scommand)
                #login="not"

            start_bit=conn.recv(2)
            
            if start_bit.hex()=='7878':
                packet_length=conn.recv(1)
                protocol=conn.recv(1)
                print(protocol.hex())
                
                if protocol.hex()=='01': #login packet complete
                    terminal_id=conn.recv(8)
                    code=conn.recv(2)
                    time_zone=conn.recv(2)
                    snol=conn.recv(2)
                    error_check=conn.recv(2)
                    stop_bit=conn.recv(2)
                    snoh=0
                    snot=0
                    snoc=0
                    if sno<65353:
                        sno+=1
                    else:
                        sno=0
                    uu=0
                    ss=""
                    snom=hex(sno)
                    for k in snom:
                        if uu>1:
                            ss=ss+k
                        uu+=1
                    if len(ss)==1:
                        ss="000"+ss
                    elif len(ss)==2:
                        ss="00"+ss
                    elif len(ss)==3:
                        ss="0"+ss
                    print(f"serial number of the message: {ss}")
                    string_crc=packet_length+protocol+terminal_id+code+time_zone+snol
                    print(f"Login packet recieved: {string_crc.hex()}")
                    bollen=crc_check(string_crc,error_check.hex())
                    if bollen:
                        nu=0
                        return_crc=""
                        for cp in hex(libscrc.x25(bytes.fromhex("0501"+ss))):
                             if nu>1:
                               return_crc=return_crc+cp
                             nu+=1
                        if len(return_crc)==3:
                            return_crc="0"+return_crc
                        elif len(return_crc)==2:
                            return_crc="00"+return_crc
                        elif len(return_crc)==1:
                            return_crc="000"+return_crc
                        response="7878"+"05"+"01"+ss+return_crc+"0d0a"
                        response=bytes.fromhex(response)
                        conn.send(response)
                        return_crc=""
                        print("response of login sent")
                        Data_Base.login_insert(terminal_id.hex(),snol.hex())
                    else:
                        print("[Invalid crc]")
                    
                elif protocol.hex()=='23':  #heart beat packet complete
                    info_content=conn.recv(1)
                    voltage_level=conn.recv(2)
                    gsm_signal=conn.recv(1)
                    port_status=conn.recv(2)
                    snoj=conn.recv(2)
                    error_check=conn.recv(2)
                    stop_bit=conn.recv(2)
                    if snoh<65353:
                        snoh+=1
                    else:
                        snoh=0
                    uu=0
                    ss=""
                    snohm=hex(snoh)
                    for k in snohm:
                        if uu>1:
                            ss=ss+k
                        uu+=1
                    if len(ss)==1:
                        ss="000"+ss
                    elif len(ss)==2:
                        ss="00"+ss
                    elif len(ss)==3:
                        ss="0"+ss
                    print(f"serial number of the message: {ss}")
                    string_crc=packet_length+protocol+info_content+voltage_level+gsm_signal+port_status+snoj
                    print(f"Heart Beat packet recieved: {string_crc.hex()}")
                    bollen=crc_check(string_crc,error_check.hex())
                    if bollen:
                        nu=0
                        for cp in hex(libscrc.x25(bytes.fromhex("0523"+ss))):
                             if nu>1:
                               return_crc=return_crc+cp
                             nu+=1
                        if len(return_crc)==3:
                               return_crc="0"+return_crc
                        elif len(return_crc)==2:
                            return_crc="00"+return_crc
                        elif len(return_crc)==1:
                            return_crc="000"+return_crc
                        response="7878"+"05"+"23"+ss+return_crc+"0d0a"
                        print(f"response sent: {response}")
                        response=bytes.fromhex(response)
                        conn.send(response)
                        return_crc=""
                        print("[response of heart beat sent]")
                        Data_Base.heartbeat_insert(info_content.hex(),voltage_level.hex(),gsm_signal.hex(),snoj.hex())
                        login="login_done"
                    else:
                        print("[Invalid crc]")
                elif protocol.hex()=='22':  #GPS packet complete
                    date_time=conn.recv(6)
                    quantity=conn.recv(1)
                    latitude=conn.recv(4)
                    longitude=conn.recv(4)
                    speed=conn.recv(1)
                    course=conn.recv(2)
                    mcc=conn.recv(2)
                    mnc=conn.recv(1)
                    lac=conn.recv(2)
                    cell_id=conn.recv(3)                    
                    acc=conn.recv(1)
                    data_upload=conn.recv(1)
                    gps_reupload=conn.recv(1)   
                    snogg=conn.recv(2)
                    error_check=conn.recv(2)
                    stop_bit=conn.recv(2)
                    print(f"Date Time: {date_time}")
                    print(f"Latitude: {latitude}, {int(latitude.hex(),16)}")
                    print(f"Longitude: {longitude}, {int(longitude.hex(),16)}")
                    print(datetime.now())
                    Data_Base.location_insert(terminal_id.hex(),datetime.now(),int(latitude.hex(),16),int(longitude.hex(),16),course.hex(),mcc.hex(),mnc.hex(),lac.hex(),cell_id.hex(),data_upload.hex(),gps_reupload.hex(),snogg.hex())
                    print("[No response]")
                elif protocol.hex()=='8a':  #time packet incomplete
                    snotg=conn.recv(2)
                    error_check=conn.recv(2)
                    stop_bit=conn.recv(2)  
                    if snot<65353:
                        snot+=1
                    else:
                        snot=0
                    uu=0
                    ss=""
                    snotm=hex(snot)
                    for k in snotm:
                        if uu>1:
                            ss=ss+k
                        uu+=1
                    if len(ss)==1:
                        ss="000"+ss
                    elif len(ss)==2:
                        ss="00"+ss
                    elif len(ss)==3:
                        ss="0"+ss
                    print(f"serial number of the message: {ss}")
                    string_crc=packet_length+protocol+snotg
                    print(f"Time packet recieved: {string_crc.hex()}")
                    bollen=crc_check(string_crc,error_check.hex())
                    if bollen:
                        nu=0
                        for cp in hex(libscrc.x25(bytes.fromhex("0b8a"+ss))):
                             if nu>1:
                               return_crc=return_crc+cp
                             nu+=1
                        if len(return_crc)==3:
                               return_crc="0"+return_crc
                        elif len(return_crc)==2:
                            return_crc="00"+return_crc
                        elif len(return_crc)==1:
                            return_crc="000"+return_crc
                        response="7878"+"05"+"8a"+ss+return_crc+"0d0a"
                        response=bytes.fromhex(response)
                        conn.send(response)
                        return_crc=""
                        print("[response of time sent]")
                    else:
                        print("[Invalid crc]")
                        
                elif protocol.hex()=='2c':  #wifi packet
                    full_packet=conn.recv(72)
                    print(f"wifi packet recieved: {full_packet.hex()}")
                    print("[No response]")
                elif protocol.hex()=='28':
                    full_packet=conn.recv(61)  #LBS packet
                    print("[No response]")

            elif start_bit=='7979':  #information transmission packet
                packet_length=conn.recv(2)
                protocol=conn.recv(1)
                print(protocol)
                length=int(packet_length.hex())
                full_packet=conn.recv(length+1)
                print(f"info packet recieved: {full_packet.hex()}")
                print("[No response]")
            
    conn.close()            





'''
            print("")
            print(f"PACKET: [{msg}]")
            print(f"Length of the packet recieved: {len(msg)}")
            msg_broken=break_msg.initial(msg.hex())
            
            
            if msg_broken[2]=='01':
                print(msg_broken)
                sno+=1
                n=crc_check.crcx25_check(msg,sno)
                print(n)
                n=bytes.fromhex(n)
                conn.send(n) 
                print("response of login sent")
                
        
            if msg_broken[2]=='23':         
                heart_beat=msg
                print(heart_beat.hex())
                sno+=1
                msg_broken=break_msg.initial(heart_beat.hex())
                print(msg_broken)
                snoh+=1
                n=crc_check.crcx25_check(msg,snoh)
                n=bytes.fromhex(n)
                print(n.hex())
                conn.send(n) 
                print("response of heart beat sent")
            if msg_broken[2]=='22':
                 gps=msg
                 print(gps)
                 sno+=1'''
            
            
            #if msg:
            
       
                #print("hi")
                #print(f"Login packet recieved and is broken down as: {msg_broken}")
                #Data_Base.login_insert(msg_broken[2],msg_broken[3],msg_broken[6])
                
            #elif msg_broken[2]=="22":
            #    print(f"Location packet recieved and bronken down as: {msg_broken}")

    
    
    
#listen for requests the send them to handler
def start():
    print(f"Server is running on: {Server}")
    server.listen()
    while True:
        
        conn, addr=server.accept()   #blocking line of code
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        print(f"Number of active connection {threading.activeCount()-1}")
        thread.start()
        
print("Server is starting..")
start() # function for listening to connections
