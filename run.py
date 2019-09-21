import krpc
from track_vessel import track_vessel
from eter import eter

conn = krpc.connect(address='localhost', rpc_port=5000, stream_port=5001)
print(conn.krpc.get_status().version)

e = eter('broker.hivemq.com', 1883)

def tick(state):
    """Every time we get a report we publish"""
    print(state)
    e.publish('VESSEL001', 'KSP_SHIP', state)

tv = track_vessel(conn)
tv.set_report_callback(tick, 0.2)
tv.start()

e.listen_blocking()
# Keep the program running...
# while True:
#     pass
