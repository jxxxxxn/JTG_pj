import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    

if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000 # server port number 
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT) # server의 주소 

    
    with socket(AF_INET, SOCK_STREAM) as client_socket: # create TCP socket for server, remote port 12000
        client_socket.connect(SERVER_ADDR)  #connect 
        
        ###################################################################
        # Receive who will start first from the server

        # server가 보낸 첫 ETTTP request message를 client_socket으로부터 받아와서 decode하고 start_send에 저장 
        # .recv(1024): 최대 1024 바이트까지 받을 수 있음 
        start_send=client_socket.recv(SIZE).decode()

        # check_msg : ETTTP 형식이 맞는지 확인 
        # msg가 ETTTP 형식이 아닌 경우, 터미널에 메시지 출력 후 client_socket을 닫음
        if check_msg(start_send,MY_IP)!=True:
            print("Message is not ETTTP format. Please reconnect!")
            client_socket.close()
            exit()


        lines=start_send.splitlines() # 받은 message를 줄 단위로 나누어서 

        for line in lines: # 매 line마다 확인 
            if line.startswith("First-Move:"): # First-Move: 로 시작하는 line을 찾아서 
                start_str=line.split(":")[1].strip() # ':'로 나눈 리스트에서 두 번째 요소를 꺼내고 공백 제거 
                break
        
        if start_str=='ME': # First_move가 'ME'이면 
            start=0
        else: # First_move가 'YOU'이면 
            start=1

        ######################### Fill Out ################################
        # Send ACK 
        
        # 보내는 입장에서는 ME와 YOU가 달라지므로 first_move라는 변수에 다시 설정 
        if start==0: # server 입장에서의 first_move가 ME, 즉 client 입장에서는 YOU 
            first_move='YOU'
        else: # server 입장에서의 first_move가 YOU, 즉 client 입장에서는 ME
            first_move='ME'

        # ETTTP 형식에 맞추어 ETTTP response message @client 전송 
        start_ack=f"ACK ETTTP/1.0 \r\nHost:{MY_IP} \r\nFirst-Move: {first_move} \r\n\r\n"
        # client_socket으로 start_send 메시지를 encode하여 전송
        client_socket.send(start_ack.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP) # GUI 관련 창 띄우기 
        root.play(start_user=start) # play 시작  
        root.mainloop()
        client_socket.close() # close connection 
        