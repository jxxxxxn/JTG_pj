<<<<<<< HEAD


import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket: # create TCP socket for server, remote port 12000
        client_socket.connect(SERVER_ADDR)  #connect 
        
        ###################################################################
        # Receive who will start first from the server
    
        start_send=client_socket.recv(SIZE).decode()

        #check_msg : ETTTP 형식이 맞는지 확인 
        if check_msg(start_send,MY_IP)!=True:
            print("Message is not ETTTP format. Please reconnect!")
            client_socket.close()
            exit()


        lines=start_send.splitlines() #받은 message를 줄 단위로 나누어서 

        for line in lines: #매 line마다 확인 
            if line.startswith("Start:"): #Start: 로 시작하는 line을 찾아서 
                start=int(line.split(":")[1].strip()) #':'로 나눈 리스트에서 두 번째 요소를 꺼내고 공백 제거, int형으로 변환 
                break

        ######################### Fill Out ################################
        # Send ACK 
        
        start_ack=f"ACK ETTTP/1.0 \r\nHost:{MY_IP}\r\nStart:{start}\r\n\r\n"
        client_socket.send(start_ack.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP) #GUI 관련 창 띄우기 
        root.play(start_user=start) #play 시작  
        root.mainloop()
        client_socket.close()
        
=======


import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
    
    
        ######################### Fill Out ################################
        # Send ACK 
        
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
>>>>>>> 1d78b5028df31a4ff2df6e2b467a29a5a31303ed
        