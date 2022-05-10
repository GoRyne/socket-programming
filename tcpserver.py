"""
해당 프로그램은 jpg 와 html 등을 처리하는 웹서버 프로그램이다.

파라미터로 포트번호를 제공한다.
"""

from socket import *
from os.path import exists,getsize
import sys

# Socket binding.
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))

serverSocket.listen(5)
while True:
  # Connect with client.
  connectionSocket, addr = serverSocket.accept()
  print("Connection : Host IP " + str(addr[0]) + ", Port " + str(addr[1]) + ", socket " + str(sys.argv[1]))
  sentence = connectionSocket.recv(65535)

  # parsing client request. 
  request_data = sentence.decode().split()
  user_agent = sentence.decode().split("User-Agent")
  sentence = str(sentence).split("\\r\\n")

  # Print status messages.
  print(request_data[0] + " " + request_data[1] + " " + request_data[2])
  print("User-Agent"+ user_agent[1].split("\r\n")[0])
  print(str(len(sentence)-3) + " headers")


  data_trans = 0
  # Issue at safari browser.
  con_type = request_data[1].split(".")[1]
  con_length = 0

  # Content-length setting.
  if exists("."+request_data[1]):
    con_length = getsize("."+request_data[1])

  # Content-type setting.
  if con_type == 'jpg':
    con_type = 'image/jpeg'
  elif con_type == 'html':
    con_type = 'text/html'

  if not exists("."+request_data[1]):
    header_400 = 'HTTP/1.0 400 NOT FOUND\r\nConnection: Close\r\nContent-length: 0\r\nContent-type: ' + con_type +'\r\n\r\n' 
    connectionSocket.send(header_400.encode())
    print("Server Error : No such file " + str(request_data[1]))
  else:
    header_200 = 'HTTP/1.0 200 0K\r\nConnection: Close\r\nContent-length: ' + str(con_length) + '\r\nContent-type: ' + con_type + '\r\n\r\n'
    connectionSocket.send(header_200.encode())
    with open("."+request_data[1], 'rb') as f:
      data = f.read(1024)
      while data:
        data_trans = connectionSocket.send(data)
        data = f.read(1024)
    print("finish " + str(con_length) + " " + str(data_trans))


  connectionSocket.close()
