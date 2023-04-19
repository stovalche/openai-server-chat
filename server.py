from array import ArrayType
import socket
import threading
import socketserver
from urllib.parse import uses_relative
import openai
import os
from IPython.display import clear_output

host = socket.gethostbyname(socket.gethostname())
port = 9900 # tells the kernel to pickup a port dynamically
BUF_SIZE = 4096
message = ""
openai.api_key = os.environ["OPENAI_API_KEY"]

user_client = {}

def ask_gpt(message):
  response = openai.Completion.create(
    engine = 'text-davinci-003',
    prompt = str(message),
    max_tokens = BUF_SIZE,
    temperature = 0
  )
  response = response.choices[0].text.strip()
  return response

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
  """ An example of threaded TCP request handler """
  def handle(self):
    while True:
      data = self.request.recv(BUF_SIZE)
      if data:
        message = data.decode('utf-8')
        cur_thread = threading.current_thread()
        id = str(cur_thread.native_id)
        if str(message).split('/')[0] == "connecttoserver12345678":
          username = str(message).split('/')[1]
          user_client.update({id: username})
          print("\n%s is joined! (Client with id %s)\n" %(user_client[id], id))
        elif message == 'exit':
          print("\n%s is exited!\n" %user_client[id])
        elif message != 'clear':
          print("%s : %s" %(user_client[id], message))
          response = str(ask_gpt(message))
          print("Server\t: %s" %response)
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
