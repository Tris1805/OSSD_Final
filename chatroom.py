import pygame
import sys
import datetime

class ChatRoom:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = []
        self.input_rect = pygame.Rect(x + 10, y + height - 30, width - 20, 20)  # Tạo ô nhập liệu
        self.input_text = ""
        self.scroll_offset = 0
        self.player = ''
        self.connect_ip = ''

    def add_message(self, player ,message):
        time = datetime.datetime.now().strftime("%H:%M:%S")
   
        full_message = player + " (" + str(time) + "): " + message
        self.messages.append(full_message)
        if len(self.messages) > 10:
            self.scroll_offset = len(self.messages) - 10

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        font = pygame.font.Font(None, 24)
        visible_messages = self.messages[self.scroll_offset:]  # Lấy tất cả các tin nhắn từ vị trí scroll_offset
        for i, message in enumerate(visible_messages):
            text = font.render(message, True, (0, 0, 0))
            text_rect = text.get_rect(topleft=(self.rect.x + 10, self.rect.y + 10 + i * 25))  # Vị trí của tin nhắn
            if text_rect.bottom <= self.rect.bottom:  # Chỉ vẽ tin nhắn nếu nó nằm trong khung chat
                surface.blit(text, text_rect)

        # Vẽ thanh cuộn nếu có nhiều hơn 10 tin nhắn
        if len(self.messages) > 10:
            pygame.draw.rect(surface, (150, 150, 150), pygame.Rect(self.rect.x + self.rect.width - 10, self.rect.y, 10, self.rect.height))
            scroll_bar_height = self.rect.height / len(self.messages) * 10
            pygame.draw.rect(surface, (100, 100, 100), pygame.Rect(self.rect.x + self.rect.width - 10, self.rect.y + self.scroll_offset / len(self.messages) * self.rect.height, 10, scroll_bar_height))

        pygame.draw.rect(surface, (255, 255, 255), self.input_rect)  # Vẽ ô nhập liệu
        if self.input_text != "":
            text = font.render(self.input_text, True, (0, 0, 0))
            surface.blit(text, (self.input_rect.x + 5, self.input_rect.y + 5))

    def handle_event(self, event, player, sock):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.input_text != "":
                    # Gửi tin nhắn lên máy chủ
                    send_data = 'CHAT-{}-{}'.format(player, self.input_text).encode()
                    sock.send(send_data)
                    # self.add_message( player + ": " + self.input_text )
                    # self.input_text = ""
            else:
                self.input_text += event.unicode

        # Xử lý thanh cuộn khi có sự kiện cuộn chuột
        if len(self.messages) > 10 and event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Cuộn lên
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.y < 0:  # Cuộn xuống
                self.scroll_offset = min(len(self.messages) - 10, self.scroll_offset + 1)

    def draw_ip(self, surface, connected_ip, position):
        # Create a font object
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        # Render the text surface
        ip_text = font.render("Connected IP: " + connected_ip, True, (0, 255, 0))
        # Get the rectangle for the text surface
        ip_rect = ip_text.get_rect(topleft=position)
        
        # Blit the text surface onto the main surface
        surface.blit(ip_text, ip_rect)
