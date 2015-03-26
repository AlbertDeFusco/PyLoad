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
  prev = {}
  instant = {}
  for net in get_interfaces():
    load[net] = list()
    prev[net] = [0,0] #rx,tx
    instant[net] = [0,0]

  print "Collecting network traffic."
  nets=''.join([("%s "%(net)) for net in get_interfaces()])
  print "Interfaces: " + nets
  print "Press ^C to terminate and generate plots"
  while(True):
    try:
      now=time.time()
      for net in get_interfaces():
        instant[net][0] = get_bytes('rx',iface=net)
        instant[net][1] = get_bytes('tx',iface=net)

        if prev[net][0]>0 and prev[net][1]>0:
	  rx_speed=instant[net][0]-prev[net][0]
	  tx_speed=instant[net][1]-prev[net][1]
	  load[net].append( (now-start,rx_speed,tx_speed) )
        #print "%10d  %10d" % (rx_speed,tx_speed)

      time.sleep(1)

      for net in get_interfaces():
        prev[net][0] = instant[net][0]
	prev[net][1] = instant[net][1]

    except KeyboardInterrupt:
      print
      print "Make graph"
      host=socket.gethostname()
      x=[l[0]/60. for l in load['eth1']]
      t=[l[1]/1024./1024. for l in load['eth1']]
      r=[l[2]/1024./1024. for l in load['eth1']]
      pyplot.plot(x,t,'b-',label='incoming')
      pyplot.plot(x,r,'r-',label='outgoing')
      pyplot.legend()
      pyplot.title(host+' eth1\nStart Time: '+date)
      pyplot.xlabel('Minutes')
      pyplot.ylabel('Network traffic (MB)')
      pyplot.savefig( 'eth0.png' )
      sys.exit()
