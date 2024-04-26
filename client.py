import pygame
from grid import Grid
import socket
import threading
import tkinter
from tkinter import messagebox
from chatroom import ChatRoom
from IDdisplay import IPDisplay
running = True

surface = pygame.display.set_mode((1100, 800))
pygame.display.set_caption("Caro-Client")
grid = Grid(20, 20)

clock = pygame.time.Clock()
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL])

chat_room = ChatRoom(820, 0, 280, 350)
ip_display = IPDisplay((820, 500))

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

HOST = '127.0.0.1'
PORT = 7776
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

player = ""
acceptPlayer = ""
isEnd = False
isStart = False
turn = False
restart = False
restartTag = "restart"

def receive_data():
    global turn, player, acceptPlayer, isEnd, isStart, restart, surface
    while True:
        data = sock.recv(1024).decode()
        data = data.split('-')
        
        if data[0] == restartTag:
                print(data)
                grid.reset_grid()
                grid.game_over = False
                restart = False
                isEnd = False
                isStart = True
                if data[1] == "disconnect":
                    messagebox.showinfo("Message", "Player disconnect")
                    isStart = False
                    player = data[2]
                    acceptPlayer = data[3]
                    connected_ip = data[4]
                    print("Connected IP: " + connected_ip)
                    if connected_ip:
                        ip_display.update_connected_ips(connected_ip)
                else:
                    acceptPlayer = data[1]

                    
                print("Accept player: ", acceptPlayer)
                if player == acceptPlayer:
                    turn = True
                continue
        # if data[0] == "IP":
        #     print(data)
        #     font = pygame.font.SysFont('Arial', 20)
        #     text_surface = font.render("Connected IP: " + data[1], True, (255, 255, 255))
        #     surface.blit(text_surface, (820,400))
        #     continue
        # else:
        #     pygame.draw.rect(surface, (0, 0, 0), (820, 360, 280, 20))

        if data[0] == "CHAT":
            nickname, message_content = data[1], data[2]        
            print (nickname , message_content)
            chat_room.add_message(nickname, message_content)
            chat_room.input_text = ""
            continue

        if len(data) >= 2 and data[0]: 
            if data[0] == "isStart":
                isStart = True  
                connected_ip = data[1]
                ip_display.add_connected_ip(connected_ip)
                continue
                        
        if len(data) <= 1 and data[0]:
            data = data[0].split('-')
            continue
        
        ## data = 2 mean set player 
        if len(data) == 3:
            player = data[0]
            acceptPlayer = data[1]
            connected_ip = data[2]
            print("Connected IP: " + connected_ip)
            if connected_ip:
                chat_room.add_message(player, connected_ip)
                ip_display.add_connected_ip(connected_ip)
            if player == acceptPlayer:
                turn = True
            send_data = '{}-{}'.format("confirm", player).encode()
            sock.send(send_data)
            continue
        # if restart:
        x, y = int(data[1]), int(data[0])
        player_recv = data[2]
        acceptPlayer = data[3]
        if acceptPlayer == player:
            turn = True
        else:
            turn = False

        print("Accept player:", acceptPlayer)

        if grid.get_cell_value(y, x) == 0:
            print("x, y, player", x, y, player_recv)
            grid.set_cell_value(y, x, player_recv)
        isEnd = data[4] == 'True'
        print("Is end:", isEnd)
        if isEnd:
            messagebox.showinfo("Message", f"{player_recv} wins!")
            print(player_recv, " wins!")

create_thread(receive_data)

while running:
    for event in pygame.event.get():
        chat_room.handle_event(event, player, sock)
        
        if event.type == pygame.QUIT:
            running = False
            
        if isStart == False:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN and not isEnd:
            print("Turn: ", turn)
            if pygame.mouse.get_pressed()[0]:
                print("Mouse pressed")
                if turn and not isEnd:
                    
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // grid.cell_height
                    col = mouse_pos[0] // grid.cell_width

                    if 0 <= row < grid.rows and 0 <= col < grid.cols:
                        #print type
                        if not grid.is_box_empty(col, row):
                            messagebox.showinfo("Message", "Box is not empty")
                            continue
                            
                        grid.get_mouse(row, col, player)
                        if grid.game_over:
                            print("Game over")
                            isEnd = True

                        send_data = '{}-{}-{}-{}-{}-{}'.format(row, col, player, acceptPlayer, isEnd, restart).encode()
                        sock.send(send_data)
                    else:
                        print("Click ngoài phạm vi ma trận")
                        continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and isEnd:
                send_data = '{}'.format(restartTag).encode()
                sock.send(send_data)
                # grid.reset_grid()
                # grid.game_over = False
                # restart = False
                # isEnd = False
    surface.fill((0,0,0))
    grid.draw(surface)
    chat_room.draw(surface)
    ip_display.draw(surface)

    clock.tick(60)
    pygame.display.flip()

    
