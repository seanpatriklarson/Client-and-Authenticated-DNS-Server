import time
import random
import sys
import hmac

import socket

# helper function that extracts the host names for each line in PROJ2-DNSTScom.txt
def extract_host(line):
  s = line.split()
  return s[0]

# helper function searches for an instance of name at the specified table and returns the index at which the name resides, or -1 otherwise
def search_table(name, table):
  x = 0
  count1 = -1
  for line in table:
      if (name == table[x]):
          count1 = x
	  return count1
      else:
	  x += 1
  return count1

def server():
  try:
      asock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[S]: Server to as socket created")
  except socket.error as err:
      print('socket open error: {}\n'.format(err))
      exit()

  try:
      csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[S]: Server to Client socket created")
  except socket.error as err:
      print('socket open error: {}\n'.format(err))
      exit()

  # declaring all the needed arrays
  input_list = []
  host_list = []
  secret_key = []

  # open file and populate the list of inputs from PROJ2-DNSTScom.txt
  with open('PROJ3-DNSTS1.txt', 'r') as f:
      input_list = []
      for line in f:
          input_list.append(line)
  f.close()

  with open('PROJ3-KEY1.txt', 'r') as f:
      secret_key = []
      for line in f:
          secret_key.append(line)
  f.close()

  # extract the host names from the file input and add them to host_list to be queried later
  for line in input_list:
      host_list.append(extract_host(line))

  asport = int(sys.argv[1])
  as_server_binding = ('', asport)
  asock.bind(as_server_binding)
  asock.listen(1)
  ashost = socket.gethostname() 
  print("[S]: Server host name is {}".format(ashost))
  localhost_ip = (socket.gethostbyname(ashost))
  print("[S]: Server IP address is {}".format(localhost_ip))
  asockid, asaddr = asock.accept()
  print ("[S]: Got a connection request from authentication server at {}".format(asaddr))

  csport = int(sys.argv[2])
  cs_server_binding = ('', csport)
  csock.bind(cs_server_binding)
  csock.listen(1)
  cshost = socket.gethostname() 
  print("[S]: Server host name is {}".format(cshost))
  localhost_ip = (socket.gethostbyname(cshost))
  print("[S]: Server IP address is {}".format(localhost_ip))
  csockid, csaddr = csock.accept()
  print ("[S]: Got a connection request from client at {}".format(csaddr))

  # receive msg from as and generate the hexdigest with the secret key and challenge word sent from as, then send the challenge back to as
  while 1:
      msg = asockid.recv(2048)
      reply = msg.decode('utf-8')
      temp = reply.split()
      challenge = temp[0]
      digest_response = hmac.new(secret_key[0].rstrip('\n').encode('utf-8'), challenge.encode('utf-8'))
      as_response = digest_response.hexdigest()
      asockid.send(as_response.encode('utf-8'))
      if (as_response == temp[1]):
          clientmsg = csockid.recv(2048)
          clientreply = clientmsg.decode('utf-8')
          name = clientreply.rstrip('\n')
          atTable = search_table(name, host_list)
          if (atTable == -1):
	      clientreply += " - Error:HOST NOT FOUND\n"
	      csockid.send(clientreply.encode('utf-8'))
          else:
	      reply = input_list[atTable]
	      csockid.send(reply.encode('utf-8'))

  # Close the server socket
  ss.close()
  exit()

server()
