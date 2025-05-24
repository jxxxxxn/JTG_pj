import random
import tkinter as tk # for GUI
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000 #server port number 
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM) #create TCP welcoming socket
    server_socket.bind(('',SERVER_PORT)) #binding with port num 
    server_socket.listen() #server begins listening for incoming TCP requests 
    MY_IP = '127.0.0.1' #server의 IP address 
    
    while True:
        # .accpet(): client로부터 접속 요청이 오면
        # 소켓 객체 client_socket, client의 IP(index0)와 포트 정보(index1) client_addr 반환 
        client_socket, client_addr = server_socket.accept() 
        
        start = random.randrange(0,2)   # select random to start, 0:server, 1:client
        
        ###################################################################
        # Send start move information to peer
    
        start_send=f"SEND ETTTP/1.0 \r\nHost: {MY_IP}\r\nStart: {start}\r\n\r\n"
        client_socket.send(start_send.encode()) 
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        # ack가 ETTTP 형식에 맞는지를 검사  
        
        start_ack=client_socket.recv(1024).decode()

        ### 이 부분 msg가 ETTTP format이 아닐 경우 다시 재요청해야하는지, 아님 이것처럼 그냥 socket 닫아버려도 되는지 애매 ###
        if check_msg(start_ack,MY_IP)!=True:
            print("Message is not ETTTP format. Please reconnect!")
            client_socket.close()
            break


        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()        
        
        client_socket.close() #close connection to to this client 
        
        break
    server_socket.close()