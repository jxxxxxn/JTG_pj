
import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):

# TTT.__init__: GUI 창 생성, 게임 시작 직전 초기화
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1                   # 초기화: my_turn = -1 : 턴이 정해지지 않은 상태

        self.geometry('500x800')            # 화면 크기 설정

        self.active = 'GAME ACTIVE'         # 게임 활성화
        self.socket = target_socket         # 상대방과 통신할 때 사용할 소켓 객체 저장
        
        self.send_ip = dst_addr             # 상대의 IP 주소 (메시지 주는 쪽)
        self.recv_ip = src_addr             # 자기 자신의 IP 주소 (메시지 받는 쪽)
        
        self.total_cells = 9                # 게임 판 cell 수 = 9
        self.line_size = 3                  # 한 줄에 3칸
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:                                              # 클라이언트용 게임 화면
            self.myID = 1   #0: server, 1: client
            self.title('34743-01-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',       # 본인 게임 화면
                     'win': 'Result: You Won!', 'text':'O','Name':"YOU"}
            self.computer = {'value': 1, 'bg': 'orange',                # 상대방
                             'win': 'Result: You Lost!', 'text':'X','Name':"ME"}   
        else:                                                   # 서버용 게임 화면
            self.myID = 0
            self.title('34743-01-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',                    # 본인 게임 화면
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}
            self.computer = {'value': self.line_size+1, 'bg': 'blue',   # 상대방
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'             # 게임 보드 GUI 구성
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()         # 게임 보드 GUI 생성 함수 호출

# 게임 보드 GUI 프레임 생성 함수
    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv QUIT 버튼 생성
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',                             # 버튼에 마우스 클릭 이벤트 연결
                              lambda e, move=i: self.my_move(e, move))  # cell 클릭 시 my_move() 함수 호출됨
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# start_user를 랜덤하게 선택해 게임을 시작하게 됨. 0:client, 1:server
    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0                             # 게임 시작 전이므로 클릭 횟수 0회

        ## frame 생성
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()

        # 상태 저장
        self.state = self.active
        if start_user == self.myID:                     # 스타트 유저가 나 라면 (선공일 경우 UI 설정)
            self.my_turn = 1                            # my_turn = 1 (True)
            self.user['text'] = 'X'                     # 버튼 눌렀을 때 표시할 텍스트: 'X'
            self.computer['text'] = 'O'                 # 상대측이 눌렀을 때 표시할 텍스트: 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']           # 내 차례이므로 'Ready' 상태
        
        else:                                           # 스타트 유저가 상대 라면 (후공일 경우 UI 설정정)
            self.my_turn = 0                            # my_turn = 0 (False)
            self.user['text'] = 'O'                     # 버튼 눌렀을 때 표시할 텍스트: 'O'
            self.computer['text'] = 'X'                 # 상대측이 눌렀을 때 표시할 텍스트: 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']            # 내 차례가 아니므로 'Hold' 상태
            _thread.start_new_thread(self.get_move,())  # 상대측 move 정보를 받는 get_move 함수 호출
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# 게임 종료 함수
    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
# 내 턴을 수행하는 함수
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move) # 반환값: 잘 보내졌는가
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0                            # 턴을 넘김
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']         
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# 상대측 턴을 받아오는 함수
    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        print("상대방의 턴을 기다리는 중...\n") 

        msg = self.socket.recv(1024).decode() # 소켓을 이용해 메시지를 받음
        # socket.recv(1024): 상대 소켓이 보낸 최대 1024 바이트의 데이터를 받아옴
        # .decode(): 바이트 -> 문자열 디코딩

        # msg valid checking: 메시지가 ETTTP 형식에 맞는지 검사
        print(f"[DEBUG] Received message: {msg}")
        msg_valid_check = False             # 메시지 유효성 검사 전 msg_valid_check 변수를 False로 초기화

        # check_msg 함수를 이용해 peer msg가 ETTTP 형식에 맞는지 검사
        if check_msg(msg, self.recv_ip):
            msg_valid_check = True          # ETTTP 형식에 맞다면 msg_valid_check = True
        
        # Message is not valid -> 프로그램 종료
        if not msg_valid_check:
            self.socket.close()             # 소켓 close
            print("msg is not valid")       # 디버깅용 메시지 - 프로그램 종료 이유: 유효하지 않은 메시지
            self.quit()                     # 게임 종료, GUI 창 닫기
        # If message is valid - send ack, update board and change turn
        else:
            # next location update in "New-Move:( , )"
            row = int(msg[msg.find('(') + 1])   # '('의 다음에 위치한 문자가 row 위치를 나타냄
            col = int(msg[msg.find(')') - 1])   # ')'의 이전에 위치한 문자가 col 위치를 나타냄
            loc = row*3 + col                   # calculate received next-move

            # ETTTP 형식에 맞추어 ETTTP response message(ACK) 전송
            low_ack = f"ACK ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"
            self.socket.send(low_ack.encode())

            print("상대방의 move msg에 대한 ACK를 보냄\n============================")
        #########################################################   
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:                     # 나의 턴이 아니라면
            self.t_debug.delete(1.0,"end")       # 텍스트박스 내용 삭제 후 함수 return 
            print("not my turn!!")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")      # 텍스트박스 내용 읽음
        d_msg = d_msg.replace("\\r\\n","\r\n")[:-1]   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")           # 텍스트박스 초기화
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''

        # 디버깅 메시지로 전송받은 메시지가 ETTTP 형식에 맞는지 검사
        if not check_msg(d_msg, self.recv_ip):
            print("wrong msg")                  # 맞지 않다면 "wrong msg" 출력 후 함수 종료
            return

        # d_msg에 적혀 있는 위치로 이동
        print("send_debug 함수 실행됨, check_msg 통과\n")
        row = int(d_msg[d_msg.find('(') + 1])   # '('의 다음에 위치한 문자가 row 위치를 나타냄
        col = int(d_msg[d_msg.find(')') - 1])   # ')'의 이전에 위치한 문자가 col 위치를 나타냄
        loc = row*3 + col                       # row와 col 값을 이용해 이동 위치 계산
        print("debug msg에 적혀 있는 위치:", row, col, loc)

        # 이동하려는 loc 위치의 칸이 '남은 칸' 리스트에 없다면
        if loc not in self.remaining_moves:
            print("already selected location\n============================")
            return                              # 이동하지 않고 함수 리턴

        '''
        Send message to peer
        '''
        # d_msg가 ETTTP 형식 검사도 통과하고, loc으로 이동 가능한 상태라면 peer에게 메시지 전송
        self.socket.send(d_msg.encode())
        print("debug msg 전송됨")
        
        '''
        Get ack
        '''
        # 보낸 d_msg에 대한 peer의 response message(ACK) 받기
        ack =  self.socket.recv(1024).decode()
        if not check_msg(ack, self.recv_ip):    # ACK를를 못 받거나 invalid한 ACK라면
            print("wrong ack")
            self.socket.close()                 # 소켓 close
            quit()                              # 게임 종료
        print("전송한 debug msg에 대한 ACK 받음\n============================")

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################

        # ETTTP 형식에 맞추어 ETTTP request message(SEND) 전송
        row_msg = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"
        self.socket.send(row_msg.encode())
        print("버튼을 눌러 메시지를 보냄\n")

        # 보낸 메시지에 대한 peer의 response message(ACK) 받기
        ack = self.socket.recv(1024).decode()
        if not check_msg(ack, self.recv_ip):        # ack을 못 받거나 invalid한 ACK라면
            print("wrong ack")
            self.socket.close()                     # 소켓 close
            quit()                                  # 게임 종료
        print("내 메시지에 대한 상대측의 ack 받음\n============================")
        
        return True                                 # move 메시지 전송을 무사히 마침: True 반환
        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        print("check_result 함수 실행됨\n")
        if not get:         # winner = 게임 오버를 먼저 발견하고 Result Poll 메시지를 보내는 host
            win = "ME"      # 본인이 winner
        else:               # loser = 상대가 이겨서 게임 오버를 나중에 발견하고 Result Poll 메시지를 받은 뒤 보내는 host
            win = "YOU"
        
        # ETTTP 형식에 맞추어 ETTTP result message(RESULT) 전송
        result_msg = f"RESULT ETTTP/1.0\r\nHost:{self.send_ip}\r\nWinner:{win}\r\n\r\n"

        if not get:
            self.socket.send(result_msg.encode())   # RESULT POLL: get=False인 경우 메시지를 먼저 전송 

            # wait peer's result msg
            peer_msg = self.socket.recv(1024).decode()
        else:
            # wait peer's result msg
            peer_msg = self.socket.recv(1024).decode()

            self.socket.send(result_msg.encode())   # 상대방의 메시지를 받은 뒤 RESULT POLL

        if not check_msg(peer_msg, self.recv_ip):   # result msg가 invalid하다면
                self.socket.close()                 # 소켓 close
                quit()                              # 게임 종료
        
        # peer의 RESULT 메시지 파싱
        print("[DEBUG]: peer msg is "+peer_msg)
        peer_result_index = peer_msg.find("Winner:")        # find where "Winner" locates
        peer_result = peer_msg[peer_result_index+7:].split("\r\n")[0].strip() # {win}이 적힌 문자열 추출

        # compare RESULT msg
        if peer_result == win:      # 서로의 Result Message 내용을 비교하고,
            return False            # (Winner=YOU)=(Winner=YOU), ME=ME 등으로 서로 다른 결과로 판단했다면 False 반환

        return True                 # 두 peer간 Result Message가 같은 Winner를 가리키고 있다면 True 반환
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip): # ETTTP 형식인지 체크하는 함수 
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################

    lines=msg.splitlines() # message를 줄 단위로 나누어서 

    if len(lines)<2: # 만약 msg가 2줄보다 적다면 (즉, SEND ETTTP/1.0만 왔다면)
        return False # ETTTP 형식 x 
    
    if not (lines[0].startswith("ACK ETTTP/1.0") or lines[0].startswith("SEND ETTTP/1.0")
        or lines[0].startswith("RESULT ETTTP/1.0")): # msg의 첫 번째 줄 검사, 3가지 경우가 아니라면 
        return False # ETTTP 형식 x 
    
    for line in lines: # 매 line마다 확인 
        if line.startswith("Host:"): # Host: 로 시작하는 line을 찾아서
            host=line.split(":")[1].strip() # ':'로 나눈 리스트에서 두 번째 요소를 꺼내고 공백 제거 
    
    if host!=recv_ip: # host와 상대방 IP가 같지 않으면 
        return False # ETTTP 형식 x 
    
    if not msg.endswith("\r\n\r\n"): # \r\n\r\n으로 끝나지 않으면  
        return False # ETTTP 형식 x 

    return True # ETTTP 형식 o
    ######################################################  
