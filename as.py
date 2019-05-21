import time
import random
import sys

import socket

def server():
  try:
      ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[S]: Server socket created")
  except socket.error as err:
      print('socket open error: {}\n'.format(err))
      exit()
  
  #try creating the .com server socket
  try:
      tss1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[S]: Server to ts1 socket created")
  except socket.error as err:
      print('socket open error: {} \n'.format(err))
      exit()

  #try creating the .edu server socket
  try:
      tss2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[S]: Server to ts2 socket created")
  except socket.error as err:
      print('socket open error: {} \n'.format(err))
      exit()

  # declaring all the needed arrays
  input_list = []
  host_list = []
  flag_list = []
  address_list = []
 
  port = int(sys.argv[1])
  ts1host = sys.argv[2]
  ts1port = int(sys.argv[3])
  ts2host = sys.argv[4]
  ts2port = int(sys.argv[5])
  server_binding = ('', port)
  ss.bind(server_binding)
  ss.listen(1)
  host = socket.gethostname() 
  print("[S]: Server host name is {}".format(host))
  localhost_ip = (socket.gethostbyname(host))
  print("[S]: Server IP address is {}".format(localhost_ip))
  csockid, addr = ss.accept()
  print ("[S]: Got a connection request from a client at {}".format(addr))

  # Get the addresses designated on the two lines with the "NS" flags, determine which address will be used for .edu and .com, and assign them to the variables eduAddr and comAddr respectively
  ts1Addr = socket.gethostbyname(ts1host)
  ts2Addr = socket.gethostbyname(ts2host)

  # binding for the ts1 and ts2 servers respectively and connect to them using the binding
  ts1_binding = (ts1Addr, ts1port)
  ts2_binding = (ts2Addr, ts2port)
  tss1.connect(ts1_binding)
  tss2.connect(ts2_binding)
  hostmsg = ts1Addr + " " + ts2Addr
  csockid.send(hostmsg.encode('utf-8'))

  # loop that is used to send all of the challenges to ts1 and ts2 from PROJ3-HNS.txt taken in from client and send back a tuple containing both responses from ts1 and ts2 to the client
  while 1:
      msg = csockid.recv(2048)
      reply = msg.decode('utf-8')
      temp = reply.split()
      tss1.send(reply.encode('utf-8'))
      ts1response = tss1.recv(2048)
      ts1msg = ts1response.decode('utf-8')
      tss2.send(reply.encode('utf-8'))
      ts2response = tss2.recv(2048)
      ts2msg = ts2response.decode('utf-8')
      if (ts1msg == temp[1].rstrip('\n')):
          resolvedmsg = "ts1"
	  csockid.send(resolvedmsg.encode('utf-8'))
      elif (ts2msg == temp[1].rstrip('\n')):
	  resolvedmsg = "ts2"
	  csockid.send(resolvedmsg.encode('utf-8'))

  # Close the server socket
  ss.close()
  exit()

server()
