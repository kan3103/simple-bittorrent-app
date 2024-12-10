
import bencodepy


class Torrent_file:
    def __init__(self):
        self.torrentfile = {}
    def add(self, info_hash ,torrent_data,upload):
        files = []
        size = 0
        if b'files' in torrent_data[b'info']:  # Multi-file torrent
            for file_info in torrent_data[b'info'][b'files']:
                file_name = (file_info[b'path'][0]).decode()
                file_length = file_info[b'length']
                size += file_length
                files.append({"name": file_name, "size": file_length, "status": upload})
        else:  # Single-file torrent
            file_name = torrent_data[b'info'][b'name'].decode()
            file_length = torrent_data[b'info'][b'length']
            files.append({"name": file_name, "size": file_length, "status": upload})

        self.torrentfile[info_hash] = {
            "tracker_url": torrent_data[b'announce'].decode(),
            "files": files,
            "total_size": sum(f["size"] for f in files),
        }
        return size

    
    def check(self, info_hash):
        if info_hash in self.torrentfile:
            return True
        
    def get(self, info_hash):
        return self.torrentfile[info_hash]
    
    def update(self, info_hash, file_index, status):
        if info_hash in self.torrentfile:
            self.torrentfile[info_hash]["files"][file_index]["status"] = status
        
    def delete(self, info_hash):
        del self.torrentfile[info_hash]