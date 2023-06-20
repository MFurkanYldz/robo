import socket
import cv2
import numpy as np
import struct

raspberry_pi_ip = "192.168.136.233"
port = 8485

# Socket'i oluştur ve bağlantıyı kur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((raspberry_pi_ip, port))
s.settimeout(10)

# Puffer boyutunu ayarla
BUFFER_SIZE = 4096

while True:
    # Veri boyutunu al
    data_size_packed = s.recv(4)
    if not data_size_packed:
        break
    data_size = struct.unpack(">L", data_size_packed)[0]

    # Veriyi al
    data = b""
    while len(data) < data_size:
        remaining_size = data_size - len(data)
        chunk = s.recv(min(BUFFER_SIZE, remaining_size))
        if not chunk:
            break
        data += chunk

    # Veriyi görüntüye dönüştür
    img_encoded = np.frombuffer(data, dtype='uint8')
    frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)

    # Görüntüyü işle
    # ...

    # Görüntüyü göster
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
