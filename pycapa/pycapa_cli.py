#!/usr/local/bin

from scapy.all import *
from kurator import zk_broker_list
from kafka import KafkaClient, KeyedProducer, RoundRobinPartitioner
from kazoo.client import KazooClient 
import argparse, struct

def make_parser():

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--topic', help='topic to produce to', dest='topic')
  parser.add_argument('-z', '--zookeeper', help='zookeeper server', dest='zookeeper')
  parser.add_argument('-l', '--local', help='print packet instead of sending to kafka', dest='local', action='store_true', default=False)
  parser.add_argument('-d', '--debug', help='enable debug messages', dest='debug', action='store_true', default=False)
  parser.add_argument('-i', '--interface', help='interface to listen on', dest='interface', required=True)
  return parser

def valid_args(args):
  if args.topic != None and args.zookeeper != None:
    return True
  else:
    return args.local

def global_header():
  return struct.pack("IHHIIII", 0xa1b2c3d4L, 2, 4, 0, 0, 65535, 1)

def packet_header(packet):
  caplen = wirelen = len(packet)
  t = time.time()
  sec = int(t)
  usec = int(round((t-sec)*1000000))
  
  return struct.pack('IIII', sec, usec, caplen, wirelen)

def formatted(s):
  hex_string =  ' '.join("{0:02x}".format(ord(c)) for c in s)
  return  '\n'.join([ hex_string[i:i+48] for i in range(0, len(hex_string), 48) ])

def local_out(packet):
  return formatted(global_header() + packet_header(packet) + str(packet)) + '\n'

def produce_callback(packet):
  '''
  callback function executed for each capture packet
  '''
  global packet_count
  global producer
  packet_count += 1
  msg = global_header() + packet_header(packet) + str(packet)
  res = producer.send(topic, packet_count, msg)
 
  if debug:
    print 'Sent %s' % packet_count
    print formatted(msg)
    print repr(msg)
    print res
  elif packet_count % 100 == 0:
    print 'Sent %s packets' % packet_count

def main():

  parser = make_parser()
  args = parser.parse_args()
  
  if not valid_args(args):
    parser.print_help()
    return

  if args.local:
    sniff(iface=args.interface, store=0, prn=local_out)
    return

  zk = KazooClient(args.zookeeper)
  zk.start()
  
  kafka = KafkaClient(zk_broker_list(zk))

  # the sniff callback only takes one parameter which is the packet
  # so everything else must be global
  global producer
  producer = KeyedProducer(kafka, partitioner=RoundRobinPartitioner)

  global packet_count
  packet_count = 0

  global topic
  topic = args.topic

  global debug
  debug = args.debug

  sniff(iface=args.interface, store=0, prn=produce_callback)

if __name__ == '__main__':
  main()
