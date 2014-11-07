import socket
import time
import pygame


CHUNK_SIZE = 5
HOST = '192.168.7.2' # ip of beaglebone USB network adapter
PORT = 50007

keys = ['\0', '\0', '\0', '\0', '\0']


pygame.init()

pygame.display.set_mode((640,480))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))

print('Connected')

def build_string():
    output = ''
    for key in keys:
        output += key
    return output

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys[1] = chr(1)
            elif event.key == pygame.K_DOWN:
                keys[2] = chr(1)
            elif event.key == pygame.K_LEFT:
                keys[3] = chr(1)
            elif event.key == pygame.K_RIGHT:
                keys[4] = chr(1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys[1] = chr(0)
            elif event.key == pygame.K_DOWN:
                keys[2] = chr(0)
            elif event.key == pygame.K_LEFT:
                keys[3] = chr(0)
            elif event.key == pygame.K_RIGHT:
                keys[4] = chr(0)
    bogus_data = build_string()
    sock.send(bogus_data)
    time.sleep(0.1)

print('exception occurred')
sock.close()
