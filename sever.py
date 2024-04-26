import socket
import threading

# Khởi tạo socket server
host = '127.0.0.1'
port = 7776
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

# Lưu trữ danh sách các client và địa chỉ IP của chúng
clients = []
ips = []

# Biến kiểm soát trạng thái kết thúc trò chơi và bắt đầu trò chơi
isEnd = False
isStart = False
restart = False

# Danh sách người chơi
players = ['X', 'O']

# Người chơi chấp nhận hiện tại
acceptPlayer = players[0]

# Hàm broadcast tin nhắn đến tất cả client
def broadcast(message):
    for client in clients:
        client.send(message)

# Hàm xử lý kết nối từ client
def handle(client, address):
    global isEnd, acceptPlayer
    while True:
        try:
            data = client.recv(1024).decode()
            data = data.split('-')
        
            print("Received", data)

            if data[0] == "restart":
                reset_grid()
                broadcast('{}-{}'.format("restart", acceptPlayer).encode())
                continue
            
            if data[0] == "CHAT":
                player = data[1]
                message = data[2]
                broadcast('{}-{}-{}'.format("CHAT", player, message).encode())
                continue
            
            if data[0] == "confirm":
                continue

            x, y = int(data[1]), int(data[0])
            player = data[2]
            acceptPlayer = data[3]

            # Đảo người chơi chấp nhận sau mỗi lượt
            acceptPlayer = players[(players.index(acceptPlayer) + 1) % len(players)]

            # Kiểm tra điều kiện kết thúc trò chơi
            if data[4] == 'True':
                isEnd = True
            else:
                isEnd = False

            # Gửi tin nhắn tới tất cả client
            broadcast('{}-{}-{}-{}-{}-{}'.format(x, y, player, acceptPlayer, isEnd, restart).encode())

        except:
            if str(address) in ips:
                ips.remove(str(address))
            # Xử lý khi client rời khỏi kết nối
            reset_grid()
            broadcast('{}-{}-{}-{}-{}'.format("restart", "disconnect", players[0], acceptPlayer, ips).encode())
            print("Client disconnected")
            

            # Xóa client khỏi danh sách clients và đóng kết nối
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break

# Hàm nhận kết nối từ client
def receive():
    global isStart, acceptPlayer
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        ips.append(str(address))  # Thêm địa chỉ IP của client vào mảng ips
        # Gửi thông tin về người chơi cho client
        client.send('{}-{}-{}'.format(players[len(clients)], acceptPlayer, ips).encode())

        # Nhận thông tin về tên người chơi từ client
        nickname = client.recv(1024).decode('utf-8')
        clients.append(client)
        print(f'Nickname of the client is {nickname}!')

        # Bắt đầu trò chơi khi đủ số lượng người chơi
        if len(clients) == 2:
            print("Start game")
            isStart = True
            broadcast('{}-{}'.format("isStart", ips).encode())

        # Khởi tạo luồng xử lý kết nối từ client
        thread = threading.Thread(target=handle, args=(client,address))
        thread.start()

# Hàm reset lại trò chơi
def reset_grid():
    global isEnd, acceptPlayer
    isEnd = False
    acceptPlayer = players[0]

# Khởi động server
print('Server is listening...')
server.listen()
receive()
