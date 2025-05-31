import random
import tkinter as tk # for GUI
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000 # server port number 
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM) # create TCP welcoming socket
    server_socket.bind(('',SERVER_PORT)) # binding with port num 
    server_socket.listen() # server begins listening for incoming TCP requests 
    MY_IP = '127.0.0.1' # server의 IP address 
    
    while True:
        # .accpet(): client로부터 접속 요청이 오면
        # 소켓 객체 client_socket, client의 IP(index0)와 포트 정보(index1) client_addr 반환 
        client_socket, client_addr = server_socket.accept() 
        
        start = random.randrange(0,2)   # select random to start, 0:server, 1:client
        
        ###################################################################
        # Send start move information to peer
    
        if start==0:
            first_move='ME'
        else:
            first_move='YOU'

        # ETTTP 형식에 맞추어 ETTTP request message @server 전송 
        start_send=f"SEND ETTTP/1.0 \r\nHost: {MY_IP} \r\nFirst-Move: {first_move} \r\n\r\n"
        
        # client_socket으로 start_send 메시지를 encode하여 전송 
        client_socket.send(start_send.encode()) 
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        # ack가 ETTTP 형식에 맞는지를 검사  
        
        # client로부터 받은 ACK를 client_socket으로부터 받아와서 decode하고 start_ack에 저장 
        # .recv(1024): 최대 1024 바이트까지 받을 수 있음 
        start_ack=client_socket.recv(1024).decode()

        # check_msg : ETTTP 형식이 맞는지 확인
        # msg가 ETTTP 형식이 아닌 경우, 터미널에 메시지 출력 후 client_socket을 닫음 
        if check_msg(start_ack,MY_IP)!=True:
            print("Message is not ETTTP format. Please reconnect!")
            client_socket.close()
            break


        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0]) # GUI 관련 창 띄우기 
        root.play(start_user=start) # play 시작  
        root.mainloop()        
        
        client_socket.close() # close connection to this client 
        
        break
    server_socket.close() # server_socket 닫음 