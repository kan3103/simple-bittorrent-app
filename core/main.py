from client import Downloader
from server import Server
import threading
import argparse
from strategy import TitOrTat
from torrent import Torrent
import requests
import os
import time
from constants import PEER_ID, PEER_PORT

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for BitTorrent peer')
    parser.add_argument('--create', type=str, help='Create a torrent file')
    parser.add_argument('--torrent',type=str, help='Specify the torrent file to download')
    parser.add_argument('--test', action='store_true', help='test the p2p network')
    parser.add_argument('--runserver', action='store_true', help='Run the server')
    parser.add_argument('--port',type=int, help='Specify the port to run the server on')
    parser.add_argument('--download', action='store_true', help='Download the torrent')
    args = parser.parse_args()

    torrents = {}
    server_thread = None
    strategy = TitOrTat()

    if args.create:
        Torrent.create_torrent_file(args.create)

    if args.runserver:
        strategy.test_init_downloaded_from()
        server = Server(torrents, args.port or 8000, strategy)
        server_thread = threading.Thread(target=server.start)
        server_thread.start()
  
    if args.download:
        time.sleep(1)
        torrent = Torrent(args.torrent)
        torrents[torrent.info_hash] = torrent
        # resp = requests.get(torrent.announce, params={'info_hash':torrent.info_hash, 'peer_id':PEER_ID, 'port':PEER_PORT}).json()
        # peers = resp['peers'] or []
        peers = [
            {'peer_id' :'DlcCX7j*$6!A,]%WF?qu', 'ip':'127.0.0.1', 'port':8000},
        ]
        downloader = Downloader(torrent, peers, strategy)
        downloader.start()
