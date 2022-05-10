"""
해당 프로그램은 웹페이지로 http GET Request를 보내며 응답 메세지를 처리합니다.

아규먼트 인자로 3가지 값을 받습니다.
1. 호스트 서버
2. 포트번호
3. 다운로드 받을 파일의 이름
"""

import socket
import sys    # For sys.exit() function when bad conditions arising and using arguments.

# Arguments condition checking.
if len(sys.argv) != 4:
  print("arguments must contain three contents")
  sys.exit()

# Setting filename for saving data.
filename = sys.argv[3].split('/')[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server status check.
try:
  sock.connect((sys.argv[1], int(sys.argv[2])))
except:
  print("{}: unknown host".format(sys.argv[1]))
  sys.exit()

# Setting http header.
request_header = "GET /"+ sys.argv[3] +" HTTP/1.0\r\n" \
"Host: " + sys.argv[1] + "\r\n" \
"User-agent: HW1/1.0\r\n\r\n" 

# Sending http GET request.
sock.send(request_header.encode())

# Get meta data.
reply = b''
data = sock.recv(254)
reply += data

headers = reply
headers = str(headers)
meta = headers.split('\\r\\n')
status = meta[0]

percent = [10,20,30,40,50,60,70,80,90,100]

                                                                  # Status code check.
if status.split(' ')[1] != "200":
  print(status.split('1.1 ')[1])
  sys.exit()

else:                                                             # File downloading
  size = meta[6]
  print("Total Size {} bytes".format(size.split(' ')[1]))
  loader = 0
  total_size = int(size.split(' ')[1])
  
  while True:
      data = sock.recv(10)
      loader += 10
      if int(loader / total_size * 100) in percent:
        print("Current Downloading {} / {} (bytes) {}%".format(loader, total_size, int(loader/total_size*100)))
        del percent[0]
      if not data:
        break
      reply += data

  with open(filename, 'wb') as f:                                 # File writing.
    print("Download Complete: {}, {}/{}".format(filename, loader, total_size))
    headers = reply.split(b'\r\n\r\n')[0]
    image = reply[len(headers)+4:]
    f.write(image)
    f.close

