import socket
import os

USER = input("Enter your name         : ")
BUF_SIZE = 4096

def echo_client(port):
  print ("Connection with %s port %s\n" %(host, port))
  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Connect the socket to the server
  server_address = (host, port)
  sock.connect(server_address)
  try:
    firstconnectmessage = "connecttoserver12345678/%s" %USER
    sock.send(firstconnectmessage.encode('utf-8'))
  except socket.error as e:
    print ("Socket error: %s" %str(e))
  except Exception as e:
    print ("Other exception: %s" %str(e))

  while True:
    try:
      # Send data
      print(USER, ": ", end='')
      message = input()
      sock.sendall(message.encode('utf-8'))
      if message == 'clear':
        os.system('clear')
      elif message == 'exit':
        sock.close()
        exit(0)
      else:
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        if amount_received < amount_expected:
          data = sock.recv(BUF_SIZE)
          amount_received += len(data)
          respose = data.decode('utf-8')
          print("ServerAI : %s" %respose)
    except socket.error as e:
      print ("Socket error: %s" %str(e))
    except Exception as e:
      print ("Other exception: %s" %str(e))

if __name__ == '__main__':
  host = input("Enter the Server's IP   : ")
  port = int(input("Enter the Server's Port : "))
  echo_client(port)
