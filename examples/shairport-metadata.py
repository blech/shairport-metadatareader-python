#!/usr/bin/env python2

# Use this script to replace MMM-ShairportMetadata script
# This will read across hosts
from time import sleep
import logging
logging.basicConfig()

from shairportmetadatareader import AirplayUDPListener
from base64 import b64encode
import json
from json import dumps
import sys
import os

ENCODING = 'utf-8'

def base64_enc(fn):
	with open(fn, 'rb') as open_file:
		byte_content = open_file.read()
	base64_bytes = b64encode(byte_content)
	return base64_bytes

def filesize(fn):
    return os.path.getsize(fn)

def on_track_info(lis, info):
    """
    Print the current track information.
    :param lis: listener instance
    :param info: track information
    """

    metadata = {}

    #if not lis.connected:
    #    print json.dumps(metadata)
    #    sys.stdout.flush()
    #    return

    metadata['Album Name'] = info['songalbum']
    metadata['Artist'] = info['songartist']
    metadata['Title'] = info['itemname']

    print json.dumps(metadata)
    sys.stdout.flush()


def on_artwork(lis, art):
    if not art:
        return

    mime = art.split(".")[-1]
    print json.dumps({"image": "data:image/" + mime + ";base64," + base64_enc(art)})
    sys.stdout.flush()

def on_connected(lis, conn):
    if not conn:
        metadata = {}
        print json.dumps(metadata)
        # Empty PNG, thanks https://png-pixel.com/
        print json.dumps({"image": "data:image/png" + ";base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="})
        sys.stdout.flush()

listener = AirplayUDPListener() # You can use AirplayPipeListener or AirplayMQTTListener

listener.bind(track_info=on_track_info) # receive callbacks for metadata changes
listener.bind(artwork=on_artwork)
listener.bind(connected=on_connected)

listener.start_listening() # read the data asynchronously from the udp server
while True:
    sleep(60) # receive data for 60 seconds
listener.stop_listening()
