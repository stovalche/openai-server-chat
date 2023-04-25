import socket
import os
import textwrap
from time import sleep

USER = input("Enter your name         : ")
BUF_SIZE = 3072

def terminal_size(opt):
  term_size_full = 50
  if str(os.get_terminal_size())[26] == ',':
    term_size_full = int(str(os.get_terminal_size())[25]) - 4
  elif str(os.get_terminal_size())[27] == ',':
    term_size_full = int(str(os.get_terminal_size())[25:27]) - 4
  elif str(os.get_terminal_size())[28] == ',':
    term_size_full = int(str(os.get_terminal_size())[25:28]) - 4

  if term_size_full <= 50:
    print("Terminal Resolution is too small!")
    sleep(3)
    exit(0)

  if term_size_full % 2 == 1:
    term_size = int((term_size_full + 1) / 2)
  else:
    term_size = int(term_size_full / 2)
  
  if opt == 'full':
    return term_size_full
  elif opt == 'half':
    return term_size
  else: return 0

  
def outputframe(value, title, align):
  term_size_full = terminal_size('full')
  term_size = terminal_size('half')

  wrapper = textwrap.TextWrapper(width=term_size)
  wordlist = wrapper.wrap(text=value)
  top_left = "\u256D"
  top_right = "\u256E"
  bot_left = "\u2570"
  bot_right = "\u256F"
  ver_line = "\u2502"
  hor_line = "\u2500"

  header = term_size - 2 - len(title)
  if header % 2 == 1:
    half_left = (header + 1) / 2
    le_left = hor_line * int(half_left)
    le_right = hor_line * int(header - half_left)
  else:
    half_left = header / 2
    le_left = hor_line * int(half_left)
    le_right = hor_line * int(header - half_left)

  foot_string = bot_left + (hor_line * (term_size + 2)) + bot_right

  if align == 'left':
    head_string = top_left + le_left + le_right + "\u257C " + title + " \u257E" + top_right
    print(f"{head_string:>{term_size_full + 4}}")
    for element in wordlist:
      space = ' ' * (term_size - len(element))
      body_string = f"{ver_line} " + element + space + f" {ver_line}"
      print(f"{body_string:>{term_size_full + 4}}")
    print(f"{foot_string:>{term_size_full + 4}}\n")
  elif align == 'right':
    head_string = top_left + "\u257C " + title + " \u257E" + le_left + le_right + top_right
    print(f"{head_string}")
    for element in wordlist:
      space = ' ' * (term_size - len(element))
      body_string = f"{ver_line} " + element + space + f" {ver_line}"
      print(f"{body_string}")
    print(f"{foot_string}\n")

def echo_client(port):
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

  os.system('clear')

  print("Welcome to ServerAi chat room!\ncommand : ")
  print("clear\t=> clear chat history,")
  print("exit\t=> exit the session.\n")
  print("Connection with %s port %s\n" %(host, port))

  while True:
    # Clear input line
    message = input("> ")
    term_size = terminal_size('full')
    ratio = len(message) / int(term_size)
    if int(ratio) < ratio:
      ratio = int(ratio) + 1
    else:
      ratio = int(ratio)
    del_line = f"\033[{ratio}A"
    print (del_line + "" + '\033[K', end="")

    # Print message in a frame
    if message != "exit" and message != "clear": sleep(0.2)
    outputframe(message, USER, 'right')
    try:
      # Send data
      sock.sendall(message.encode('utf-8'))
      if message == 'clear':
        os.system('clear')
      elif message == 'exit':
        os.system('clear')
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
          outputframe(respose, "ServerAi", "left")
    except socket.error as e:
      print ("Socket error: %s" %str(e))
    except Exception as e:
      print ("Other exception: %s" %str(e))

if __name__ == '__main__':
  host = input("Enter the Server's IP   : ")
  port = int(input("Enter the Server's Port : "))
  echo_client(port)
