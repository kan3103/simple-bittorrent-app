import os
import bencodepy, hashlib
from utils import generate_pieces
from constants import PIECE_SIZE, TRACKER_URL


def list_files_with_paths(directory):
    result = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            # Add files as individual lists
            result.append([entry])
        elif os.path.isdir(full_path):
            # Add directories and their contents
            sub_files = os.listdir(full_path)
            result.append([entry] + sub_files)
    return result

   
def decode_bencoded(data):
    if isinstance(data, dict):
        return {
            key.decode('utf-8'): decode_bencoded(value) if key != b'pieces' else value
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [decode_bencoded(item) for item in data]
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        return data  # Leave other types (e.g., integers) unchanged

class Torrent:
    def __init__(self, torrent_file):
        with open(torrent_file, "rb") as f:
            data = f.read()
        torrent = decode_bencoded(bencodepy.decode(data))
        self.torrent_data = bencodepy.decode(data)
        self.name = torrent['info']['name']
        os.makedirs(self.name, exist_ok=True)
        self.announce = torrent['announce']
        self.piece_length = torrent['piece length']
        self.files = torrent['info']['files']
        self.files_info = [{"downloaded": 0, "length": file['length'], "path": self.name + os.sep + os.path.join(*file['path'])} for file in self.files]
        self.pieces = [torrent['pieces'][i:i+20] for i in range(0, len(torrent['pieces']), 20)]
        self.info_hash = hashlib.sha1(bencodepy.encode(torrent['info'])).digest()
    
    @staticmethod
    def create_torrent_file(directory):
        files  = list_files_with_paths(directory)
        print(files)
        torrent_dict = {
            "announce": TRACKER_URL,
            "info": {
                "name": directory,  # Name of the torrent, usually the folder name
                "files": [{"length": os.path.getsize(directory+ os.sep + os.path.join(*file)), "path": file} for file in files],
            },
            "pieces": b''.join(generate_pieces([directory + os.sep + os.path.join(*file) for file in files])),
            "piece length": PIECE_SIZE
        }

        # Encode and save as .torrent
        encoded_torrent = bencodepy.encode(torrent_dict)
        torrent_file = directory + ".torrent"
        try:
            with open(torrent_file, "wb") as f:
                f.write(encoded_torrent)
                print(f"Torrent file created: {torrent_file}")
        except Exception as e:
            print(f"Error creating torrent file: {e}")
    
        return Torrent(torrent_file)
    