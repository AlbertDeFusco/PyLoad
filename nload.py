#!/usr/bin/env python

import time
import sys
import socket
import os
import netifaces
from matplotlib import pyplot

def get_interfaces():
  interfaces=list()
  for net in netifaces.interfaces():
    if net != 'lo':
      interfaces.append(net)
  return interfaces


def get_bytes(t, iface='eth0'):
  with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
    data = f.read();
    return int(data)

if __name__ == '__main__':
  start=time.time()
  date= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start))


  load = {}
  for net in get_interfaces():
    load[net] = list()
    prev[net] = (0,0)

  rx_prev=0
  tx_prev=0

  print "Collecting network traffic."
  print "Interfaces :" + get_interfaces()
  print "Press ^C to terminate and generate plots"
  while(True):
    try:
      now=time.time()
      tx = get_bytes('tx')
      rx = get_bytes('rx')

      if rx_prev>0 and tx_prev>0:
        rx_speed=rx-rx_prev
        tx_speed=tx-tx_prev
	load.append( (now-start,rx_speed,tx_speed) )
        #print "%10d  %10d" % (rx_speed,tx_speed)

      time.sleep(1)

      tx_prev = tx
      rx_prev = rx
    except KeyboardInterrupt:
      print
      print "Make graph"
      host=socket.gethostname()
      x=[l[0]/60. for l in load]
      t=[l[1]/1024./1024. for l in load]
      r=[l[2]/1024./1024. for l in load]
      pyplot.plot(x,t,'r-',label='recieve')
      pyplot.plot(x,r,'b-',label='send')
      pyplot.legend()
      pyplot.title(host+' eth0\nStart Time: '+date)
      pyplot.xlabel('Minutes')
      pyplot.ylabel('Network traffic (MB)')
      pyplot.savefig( 'eth0.png' )
      sys.exit()
