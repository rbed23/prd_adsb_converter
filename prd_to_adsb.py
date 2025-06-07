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
