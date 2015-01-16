# Pycapa

## Overview

Pycapa is an open source tool to handle packet capture ingestion for [OpenSOC](https://github.com/opensoc/opensoc-streaming). It is intended as a testing and development tool. It is not performant enough for production operations. The tool will capture packets from a specified interface and push them into a Kafka Topic in a format understandable by OpenSOC's PcapParserBolt.

## Requirements

* [Scapy](http://www.secdev.org/projects/scapy/)
* [kurator](https://github.com/tpiscitell/kurator)

## Installation

First install the required packages with pip:
    
    pip install -r requirements.txt

Then install pycapa:

    python setup.py install

## Usage

    usage: pycapa.py [-h] [-t TOPIC] [-z ZOOKEEPER] [-l] [-d] -i INTERFACE

    optional arguments:
      -h, --help            show this help message and exit
      -t TOPIC, --topic TOPIC
                            topic to produce to
      -z ZOOKEEPER, --zookeeper ZOOKEEPER
                            zookeeper server
      -l, --local           print packet instead of send to kafka
      -d, --debug           enable debug messages
      -i INTERFACE, --interface INTERFACE
                            interface to listen on

## Kafka Message Format

Each kafka message corresponds to a single packet capture from the wire. A kafka message can be thought of as a single packet [libpcap](http://wiki.wireshark.org/Development/LibpcapFileFormat) capture file. It contains the Global Header, the Packet Header, and the packet data.
