import krpc
from track_vessel import track_vessel

conn = krpc.connect(address='localhost', rpc_port=5000, stream_port=5001)
print(conn.krpc.get_status().version)
