# pip install flask to install

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

PEER_FILE = "file_peers.json"
file_peers = {}  # Format: {"info_hash1": [{"peer_id": "peer123", "port": 8080}, ...]}

def load_peers():
    global file_peers
    if os.path.exists(PEER_FILE):
        with open(PEER_FILE, "r") as f:
            file_peers = json.load(f)
            print(f"Loaded peer list from {PEER_FILE}: {file_peers}")
    else:
        print("Peer file not found, starting with an empty list.")

def save_peers():
    with open(PEER_FILE, "w") as f:
        json.dump(file_peers, f, indent=4)
        print(f"Saved peer list to {PEER_FILE}.")

def remove_peer(info_hash, peer_id, port):
    if info_hash in file_peers:
        peer_list = file_peers[info_hash]
        for peer in peer_list:
            if peer["peer_id"] == peer_id and peer["port"] == port:
                peer_list.remove(peer)
                if not peer_list:  
                    del file_peers[info_hash]
                save_peers()
                return True
    return False

@app.route("/", methods=["GET"])
def index():
    return "Tracker is running"


@app.route("/announce", methods=["GET"])
def handle_event():
    info_hash = request.args.get("info_hash")
    peer_id = request.args.get("peer_id")
    port = request.args.get("port")
    event = request.args.get("event")
    
    if not info_hash:
        return jsonify({"error": "Info hash is required"}), 400

    if port:
        try:
            port = int(port)
        except ValueError:
            return jsonify({"error": "Port must be int"}), 400

    if event == "started":
        if not peer_id or not port:
            return jsonify({"error": "peer_id and port is required"}), 400
        if info_hash not in file_peers:
            file_peers[info_hash] = []
        return jsonify({'peers': file_peers[info_hash]})

    elif event == "stopped":
        if not peer_id or not port:
            return jsonify({"error": "peer_id and port is required "}), 400
        removed = remove_peer(info_hash, peer_id, port)
        return jsonify({"success": removed})
    
    elif event == "completed":
        if not peer_id or not port:
            return jsonify({"error": "peer_id and port is required"}), 400
        
        if info_hash not in file_peers:
            file_peers[info_hash] = []
        
        if not any(peer["peer_id"] == peer_id and peer["port"] == port for peer in file_peers[info_hash]):
            file_peers[info_hash].append({"peer_id": peer_id, "ip" : request.remote_addr, "port": port})
            save_peers()
        
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Invalid event"}), 400

if __name__ == "__main__":
    load_peers()
    app.run(host="0.0.0.0", port=8080)
