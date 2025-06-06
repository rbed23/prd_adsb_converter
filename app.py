#!/usr/bin/env python3
"""
This is a simple script that connects to a UDP socket to listen for incoming PRD messages
and converts to them a ADS-B-compatible format.
The ADS-B message is then re-transmitted out a specified UDP port.

It uses the `socket` library to create a UDP socket and listen for incoming messages.

Author: Ryan Bednar <rbed23@gmail.com>
Version: 0.1.0
"""
import argparse
from datetime import datetime
import logging
import requests
import socket
import sys

from prd_to_adsb import convert_prd_to_adsb, PRDMessage, ADSBMessage


def main():
    parser = argparse.ArgumentParser(description="Convert PRD messages to ADS-B format and retransmit.")
    parser.add_argument("--callsign", type=str, default="ABC123",
                        help="Callsign to use for ADS-B messages.")
    parser.add_argument("--host", type=str, default="localhost",
                        help="Host to bind the UDP socket to.")
    parser.add_argument("--port", type=int, default=5000,
                        help="Port to bind the UDP socket to.")
    parser.add_argument("--adsb_host", type=str, default="localhost",
                        help="Host to bind ADS-B messages to.")
    parser.add_argument("--adsb_port", type=int, default=80,
                        help="Port to send ADS-B messages to.")
    parser.add_argument("--log_level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level.")
    args = parser.parse_args()

    # Configure logging
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, args.log_level, logging.DEBUG))  # Set the level for console output
    logger.addHandler(console_handler)

    # File handler
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_handler = logging.FileHandler(f'logs/app_{dt}.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, args.log_level, logging.INFO))  # Set the level for file output
    logger.addHandler(file_handler)

    logger.info(f"\n---------------------------------------------------\n"
                f"Starting PRD to ADS-B conversion service"
                f"{f' [{args.log_level.upper()}]' if args.log_level.upper() != 'INFO' else ''}...\n"
                f"---------------------------------------------------")

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.host, args.port))
    logger.info(f"Listening for PRD messages on {args.host}:{args.port}...")

    logger.info(f"Forwarding converted ADS-B messages to {args.adsb_host}:{args.adsb_port}...")

    while True:
        try:
            # Receive PRD message
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            logger.debug (f"Received PRD message from {addr}: {data}")

            # Convert PRD message to ADS-B format
            prd_message = PRDMessage.from_bytes(data)
            logger.debug(f"PRD message: {prd_message}")

            adsb_message = convert_prd_to_adsb(prd_message)
            logger.debug(f"Converted ADS-B message: {adsb_message}")

            # Send ADS-B message
            requests.post(f"http://{args.adsb_host}:{args.adsb_port}/adsb", json=dict(adsb_message))
            logger.info(f"Sent ADS-B message: {adsb_message}")

        except KeyboardInterrupt:
            logger.info("Exiting...\n\n")
            break
        except Exception as e:
            logger.error(f"Error: {(e,)}")


if __name__ == "__main__":
    main()
