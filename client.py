import time
import random
import sys
import hmac

import socket

# helper function that extracts the hostname at the specified line of input
def extract_key(line):
  s = line.split()
  return s[0]

# helper function that extracts the IP addresses at used for each line in PROJ2-DNSRS.txt
def extract_challenge(line):
  a = line.split()
  return a[1]

# helper function that extracts the flag at the specified line of input (either 'A' or 'NS')
def extract_query(line):
  flag = line.split()
  return flag[2]

def client():
  try:
      cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[C]: Client to as socket created")
  except socket.error as err:
      print('socket open error: {} \n'.format(err))
      exit()

  try:
      tss1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[C]: Client to ts1 socket created")
  except socket.error as err:
      print('socket open error: {} \n'.format(err))
      exit()

  try:
      tss2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[C]: Client to ts2 socket created")
  except socket.error as err:
      print('socket open error: {} \n'.format(err))
      exit()
  
  # read from the file and populate the lines of data into an array
  input_list = []
  key_list = []
  challenge_list = []
  query_list = []
  key_challenge_list = []
  encoded_challenge_list = []
  encoded_list = []
  as_input_list = []
  with open('PROJ3-HNS.txt', 'r') as f:  
      for line in f:
	  input_list.append(line)
  f.close()

  # extract the file input into the three necessary arrays
  for line in input_list:
      key_list.append(extract_key(line))
      challenge_list.append(extract_challenge(line))
      query_list.append(extract_query(line))
      key_challenge_list.append((extract_key(line), extract_challenge(line)))

  # create a list of tuples (challenge, hexdigest) with encodings for the challenges to be sent to as server
  for line in key_challenge_list:
     digest_query = hmac.new(line[0].encode("utf-8"), line[1].encode("utf-8"))
     encoded_list.append(digest_query.hexdigest())
     encoded_challenge_list.append((line[1], digest_query.hexdigest()))
  
  # list of inputs to be sent to the as server
  for line in encoded_challenge_list:
      as_input_list.append(line[0] + " " + line[1])

  # Define the two ports on which you want to connect to the server
  ashostname = sys.argv[1]
  asport = int(sys.argv[2])
  ts1port = int(sys.argv[3])
  ts2port = int(sys.argv[4])
  as_addr = socket.gethostbyname(ashostname)

  # connect to the as, ts1, ts2 servers
  as_server_binding = (as_addr, asport)
  cs.connect(as_server_binding)
  msg = cs.recv(2048)
  hostmsg = msg.decode('utf-8')
  hosts = hostmsg.split()
  ts1host = hosts[0]
  ts2host = hosts[1]
  ts1_addr = socket.gethostbyname(ts1host)
  ts2_addr = socket.gethostbyname(ts2host)
  ts1_server_binding = (ts1_addr, ts1port)
  ts2_server_binding = (ts2_addr, ts2port)
  tss1.connect(ts1_server_binding)
  tss2.connect(ts2_server_binding)

  # send data to file RESOLVED.txt
  newFile = open('RESOLVED.txt', 'w')
  for i in range(len(input_list)):
      msg = as_input_list[i]
      tempdigest = msg.split()
      msgdigest = tempdigest[1]
      cs.send(msg.encode('utf-8'))
      data_from_as = cs.recv(2048)
      reply = data_from_as.decode('utf-8')
      if (reply == "ts1"):
	  name = query_list[i]
          tss1.send(name.encode('utf-8'))
          reply = tss1.recv(2048)
	  response_from_ts1 = reply.decode('utf-8')
          newFile.write(response_from_ts1)
      elif (reply == "ts2"):
          name = query_list[i]
          tss2.send(name.encode('utf-8'))
          reply = tss2.recv(2048)
	  response_from_ts2 = reply.decode('utf-8')
          newFile.write(response_from_ts2)

   

  # close the client socket
  cs.close()
  exit()

client()

