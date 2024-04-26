import pygame
import threading

class IPDisplay:
    def __init__(self, position):
        self.position = position
        self.font = pygame.font.Font('freesansbold.ttf', 14)
        self.connected_ips = []
        self.lock = threading.Lock()

    def add_connected_ip(self, ip_port_list):
        with self.lock:
            ip_port_list = eval(ip_port_list)
            for item in ip_port_list:
                ip, port = eval(item)  # Evaluate each item to extract the IP and port
                if (ip, port) not in self.connected_ips:
                    self.connected_ips.append((ip, port))

    def remove_connected_ip(self, ip, port):
        with self.lock:
            if (ip, port) in self.connected_ips:
                self.connected_ips.remove((ip, port))

    def update_connected_ips(self, ip_port_list):
        with self.lock:
            self.connected_ips = []
            ip_port_list = eval(ip_port_list)
            for item in ip_port_list:
                ip, port = eval(item)
                self.connected_ips.append((ip, port))

    def draw(self, surface):
        y_offset = 0
        with self.lock:
            for ip, port in self.connected_ips:
                ip_text = self.font.render(f"('{ip}', {port})", True, (0, 255, 0))
                ip_rect = ip_text.get_rect(topleft=(self.position[0], self.position[1] + y_offset))
                surface.blit(ip_text, ip_rect)
                y_offset += 20  # Increase the y offset for the next IP address
