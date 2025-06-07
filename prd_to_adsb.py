#!/usr/bin/env python3
"""

"""
import yaml


try:
    # Load the callsign to icon mapping from a YAML file
    with open("config/callsigns_to_icons.yaml", "r") as file:
        CALLSIGN_TO_ICON = yaml.safe_load(file)
except FileNotFoundError:
    print("No callsigns_to_icons.yaml config file found, using default unknown icon(s).")
    callsign_icons = {}
else:
    # ensure all callsign keys are uppercase
    callsign_icons = dict([(call.upper(), link) for call, link in CALLSIGN_TO_ICON.items()])


DEFAULT_UNKNOWN_AIRCRAFT_ICON = "assets/icons/circle.svg"


def init_objects(obj, kwargs):
    """
    Initialize an object with attributes from a dictionary.

    Args:
        obj: The object to initialize.
        kwargs: A dictionary containing attribute names and values.
    """
    prd_fields = ['callsign', 'type', 'latitude', 'longitude', 'altitude', 'speed', 'heading']

    # Set default values for fields if not provided in kwargs
    for field in prd_fields:
        if field == 'callsign':
            setattr(obj, field, kwargs.get(field, "ABC123"))
        elif field =='type':
            setattr(obj, field, kwargs.get(field, "Unknown"))
        else:
            setattr(obj, field, kwargs.get(field, 0.0))
        kwargs.pop(field, None)  # Remove the field from kwargs after setting it

    # Set any additional attributes from kwargs
    for key, value in kwargs.items():
        setattr(obj, key, value) if not hasattr(obj, key) else None

    # Set the icon based on callsign or type, else DEFAULT UNKNOWN_AIRCRAFT_ICON
    obj.icon = callsign_icons.get(obj.callsign.upper(),  # try callsign to get icon
                                  callsign_icons.get(obj.type,  # try type to get icon
                                                     DEFAULT_UNKNOWN_AIRCRAFT_ICON))


class ADSBMessage:
    """
    A class representing an ADS-B message.
    This is a placeholder for the actual implementation.

    Attributes:
    more details can be found at:
    https://github.com/flightaware/dump1090/blob/master/README-json.md#aircraftjson


    now: the time this file was generated, in seconds since Jan 1 1970 00:00:00 GMT (the Unix epoch).
    messages: the total number of Mode S messages processed since dump1090 started.
    aircraft: an array of JSON objects, one per known aircraft. Each aircraft has the following keys. Keys will be omitted if data is not available.
        hex: the 24-bit ICAO identifier of the aircraft, as 6 hex digits. The identifier may start with '~', this means that the address is a non-ICAO address (e.g. from TIS-B).
        type: type of underlying message, one of:
            adsb_icao: messages from a Mode S or ADS-B transponder, using a 24-bit ICAO address
            adsb_icao_nt: messages from an ADS-B equipped "non-transponder" emitter e.g. a ground vehicle, using a 24-bit ICAO address
            adsr_icao: rebroadcast of ADS-B messages originally sent via another data link e.g. UAT, using a 24-bit ICAO address
            tisb_icao: traffic information about a non-ADS-B target identified by a 24-bit ICAO address, e.g. a Mode S target tracked by secondary radar
            adsb_other: messages from an ADS-B transponder using a non-ICAO address, e.g. anonymized address
            adsr_other: rebroadcast of ADS-B messages originally sent via another data link e.g. UAT, using a non-ICAO address
            tisb_other: traffic information about a non-ADS-B target using a non-ICAO address
            tisb_trackfile: traffic information about a non-ADS-B target using a track/file identifier, typically from primary or Mode A/C radar
        flight: callsign, the flight name or aircraft registration as 8 chars (2.2.8.2.6)
        alt_baro: the aircraft barometric altitude in feet
        alt_geom: geometric (GNSS / INS) altitude in feet referenced to the WGS84 ellipsoid
        gs: ground speed in knots
        ias: indicated air speed in knots
        tas: true air speed in knots
        mach: Mach number
        track: true track over ground in degrees (0-359)
        track_rate: Rate of change of track, degrees/second
        roll: Roll, degrees, negative is left roll
        mag_heading: Heading, degrees clockwise from magnetic north
        true_heading: Heading, degrees clockwise from true north
        baro_rate: Rate of change of barometric altitude, feet/minute
        geom_rate: Rate of change of geometric (GNSS / INS) altitude, feet/minute
        squawk: Mode A code (Squawk), encoded as 4 octal digits
        emergency: ADS-B emergency/priority status, a superset of the 7x00 squawks (2.2.3.2.7.8.1.1)
        category: emitter category to identify particular aircraft or vehicle classes (values A0 - D7) (2.2.3.2.5.2)
        nav_qnh: altimeter setting (QFE or QNH/QNE), hPa
        nav_altitude_mcp: selected altitude from the Mode Control Panel / Flight Control Unit (MCP/FCU) or equivalent equipment
        nav_altitude_fms: selected altitude from the Flight Manaagement System (FMS) (2.2.3.2.7.1.3.3)
        nav_heading: selected heading (True or Magnetic is not defined in DO-260B, mostly Magnetic as that is the de facto standard) (2.2.3.2.7.1.3.7)
        nav_modes: set of engaged automation modes: 'autopilot', 'vnav', 'althold', 'approach', 'lnav', 'tcas'
        lat, lon: the aircraft position in decimal degrees
        nic: Navigation Integrity Category (2.2.3.2.7.2.6)
        rc: Radius of Containment, meters; a measure of position integrity derived from NIC & supplementary bits. (2.2.3.2.7.2.6, Table 2-69)
        seen_pos: how long ago (in seconds before "now") the position was last updated
        version: ADS-B Version Number 0, 1, 2 (3-7 are reserved) (2.2.3.2.7.5)
        nic_baro: Navigation Integrity Category for Barometric Altitude (2.2.5.1.35)
        nac_p: Navigation Accuracy for Position (2.2.5.1.35)
        nac_v: Navigation Accuracy for Velocity (2.2.5.1.19)
        sil: Source Integity Level (2.2.5.1.40)
        sil_type: interpretation of SIL: unknown, perhour, persample
        gva: Geometric Vertical Accuracy (2.2.3.2.7.2.8)
        sda: System Design Assurance (2.2.3.2.7.2.4.6)
        modea: true if we seem to be also receiving Mode A responses from this aircraft
        modec: true if we seem to be also receiving Mode C responses from this aircraft
        mlat: list of fields derived from MLAT data
        tisb: list of fields derived from TIS-B data
        messages: total number of Mode S messages received from this aircraft
        seen: how long ago (in seconds before "now") a message was last received from this aircraft
        rssi: recent average RSSI (signal power), in dbFS; this will always be negative.



    now         timestamp created   (float optional)
    hex         ICAO Identifier     (String optional)
    flight      IDENT Identifier    (String optional - name of plane)
    alt_baro    barometric alt (feet)   (int optional - altitude)
    alt_geom (int optional)
    track (int optional)
    baro_rate (int optional)
    category (string optional)
    nav_qnh (float optional)
    nav_altitude_mcp (int optional)
    nav_heading (float optional)
    nic (int optional)
    rc (int optional)
    seen_pos (float optional)
    version (int optional)
    nic_baro (int optional)
    nac_p (int optional)
    nac_v (int optional)
    sil (int optional)
    sil_type (string optional)
    mlat (array optional)
    tisb (array optional)
    messages (int optional)
    seen        timestamp reported  (float optional)
    rssi (float optional)
    squawk (optional) - look at # conversion 7600, 7700, 4000, 5000, 7777, 6100, 5400, 4399, 4478, ...)
    speed       ground speed (knts)     (optional)
    mach (optional speed, mac to mph *767)
    emergency (optional string)
    lat         latitude        (long optional)
    lon         longitude       (long optional)
    """
    callsign = ""
    type = ""
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0
    speed = 0.0
    heading = 0.0
    icon = ""
    tail_number = ""

    def __init__(self, **kwargs):
        """ Initialize an ADSBMessage instance."""
        init_objects(self, kwargs)
        if not hasattr(self, 'tail_number'):
            self.tail_number = "N/A"
        if hasattr(callsign_icons, self.tail_number.upper()):
            self.icon = callsign_icons[self.tail_number.upper()]

    def __str__(self):
        """
        String representation of the ADSBMessage instance.

        Returns:
            str: A string representation of the ADSBMessage.
        """
        return f"{dict([(k,v) for k, v in self.__dict__.items() if k != 'icon'])}"

    def __repr__(self):
        return (f"ADSBMessage(callsign={self.callsign}, tail={self.tail_number}, "
                f"latitude={self.latitude}, longitude={self.longitude}, "
                f"altitude={self.altitude}, speed={self.speed}, heading={self.heading}, "
                f"type={self.type}, icon={self.icon})")

    def __iter__(self):
        return iter(self.__dict__.items())


class PRDMessage:
    """
    A class representing a PRD message.
    This is a placeholder for the actual implementation.
    """
    callsign = ""
    type = ""
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0
    speed = 0.0
    heading = 0.0
    icon = ""

    def __init__(self, **kwargs):
        """ Initialize a PRDMessage instance."""
        init_objects(self, kwargs)

    def to_dict(self) -> dict:
        """
        Convert the PRDMessage instance to a dictionary.

        Returns:
            dict: A dictionary representation of the PRDMessage.
        """
        return {
            'callsign': self.callsign,
            'type': self.type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'speed': self.speed,
            'heading': self.heading,
            'icon': self.icon
        }

    @staticmethod
    def from_bytes(data: bytes) -> 'PRDMessage':
        # Placeholder for converting bytes to PRDMessage
        return PRDMessage()


def convert_prd_to_adsb(prd_message: PRDMessage) -> ADSBMessage:
    """
    Convert a PRD message to an ADS-B message.

    Args:
        prd_message (PRDMessage): The PRD message to convert.

    Returns:
        ADSBMessage: The converted ADS-B message.
    """
    return ADSBMessage(**prd_message.to_dict())
