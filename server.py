import socket
import threading
import socketserver
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
host = socket.gethostbyname(socket.gethostname())
port = 9900 # tells the kernel to pickup a port dynamically
BUF_SIZE = 3072
message = ""
user_client = {}

hcheck = host.split('.')
if hcheck[0] + '.' + hcheck[1] + '.' + hcheck[2] == '127.0.0':
  host = 'localhost'

def ask_gpt(message):
  try:
    openai_ans = openai.Completion.create(
      engine = 'text-davinci-003',
      prompt = str(message),
      max_tokens = BUF_SIZE,
      temperature = 0
    )
    return str(openai_ans.choices[0].text.strip())
  except Exception as e:
    return str(e)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
  """ An example of threaded TCP request handler """
  def handle(self):
    while True:
      data = self.request.recv(BUF_SIZE)
      if data:
        message = str(data.decode('utf-8'))
        cur_thread = threading.current_thread()
        id = str(cur_thread.native_id)
        if str(message).split('/')[0] == "connecttoserver12345678":
          username = str(message).split('/')[1]
          user_client.update({id: username})
          print("\n%s is joined! (Client with id %s)\n" %(user_client[id], id))
        elif message == 'exit':
          print("\n%s is exited! (Client with id %s)\n" %(user_client[id], id))
        elif message != 'clear':
          print("%s : %s" %(user_client[id], message))
          response = ask_gpt(message)
          print("Server : %s" %response)
          self.request.sendall(bytes(response, 'utf-8'))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  """ Nothing to add here, inherited everything necessary from parents """
  pass

if __name__ == "__main__":
  # Run server
  server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)

  # Start a thread with the server -- one thread per request
  server_thread = threading.Thread(target = server.serve_forever)
  # Exit the server thread when the main thread exist
  server_thread.daemon = True
  server_thread.start()
  print("Server loop running on %s on %s, port %s. " %(server_thread.name, host, port))
  
  while 1:
    pass
