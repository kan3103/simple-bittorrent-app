# Description: Constants used in the node module
import os
import socket

PROTOCOL_NAME = 'BitTorrent protocol'
PEER_ID = 'peer5678901234567890'
PEER_IP = socket.gethostbyname(socket.gethostname()) or 'localhost'
PEER_PORT = 8000
TRACKER_URL = 'http://10.0.16.149:8080/announce'
# TRACKER_URL = 'http://172.16.0.165/8001/announce'
PIECE_SIZE = 524288 # 512 KB
BLOCK_SIZE = 16384 # 16 KB
# PIECE_SIZE =  100
# BLOCK_SIZE = 50