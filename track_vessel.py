from threading import Timer

class track_vessel:
    """Track different vessel readings and report consolidated state"""

    def __init__(self, conn, vessel=None):
        self.conn = conn
        # Here we keep the latest vessel state
        self.state = {}

        self.track_vessel(vessel)
        self.set_read_callbacks()


    def track_vessel(self, vessel=None):
        if vessel is None:
            self.track_active_vessel()
        else:
            self.vessel = vessel
        
        self.flight_info = self.vessel.flight()
        self.refframe = self.vessel.orbit.body.reference_frame

    def track_active_vessel(self):
        self.vessel = self.conn.space_center.active_vessel


    def set_read_callbacks(self):
        self.position = self.conn.add_stream(self.vessel.position, self.refframe)
        self.position.add_callback(self.tick_position)

        self.altitude = self.conn.add_stream(getattr, self.flight_info, 'mean_altitude')
        self.altitude.add_callback(self.tick_altitude)

    def tick_position(self, position):
        """When we receive a position report we update internal state"""
        self.state['position'] = position

    def tick_altitude(self, altitude):
        """When we receive an altitude report we update internal state"""
        self.state['altitude'] = altitude


    def set_report_callback(self, callback, s_delay = 0.1):
        """Set a callback to be called every s_delay seconds"""
        self.callback = callback
        self.s_delay = s_delay

    def report(self):
        """Call the registered callback with the full current state"""
        Timer(self.s_delay, self.report).start()
        self.callback(self.state)


    def start(self):
        """Start streams and timers"""
        if self.position: self.position.start()
        if self.altitude: self.altitude.start()
        if self.callback: self.report()
