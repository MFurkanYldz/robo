import socket
import cv2
import struct



# IP kameradan görüntü al
cap = cv2.VideoCapture('http://192.168.136.32:8080/video')

# Socket puffer boyutunu ayarla
BUFFER_SIZE = 4096

# Socket'i oluştur ve bağlantıyı kabul et
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)

server_socket.bind((host_ip, 8485))
server_socket.listen(0)

while True:
    client, addr = server_socket.accept()

    while cap.isOpened():
        ret, frame = cap.read()

        # Görüntünün boyutunu yarıya indirge
        frame = cv2.resize(frame, (640,480))

        # frame'i JPEG formatına dönüştür ve sıkıştırma kalitesini ayarla
        _, img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

        # frame'i byte dizisine dönüştür
        data = img_encoded.tobytes()

        # data boyutunu paketle ve gönder
        size = len(data)
        size_packed = struct.pack(">L", size)
        client.sendall(size_packed)

        # Veriyi parçalar halinde gönder
        offset = 0
        while offset < size:
            chunk = data[offset:offset+BUFFER_SIZE]
            client.sendall(chunk)
            offset += len(chunk)

    client.close()
