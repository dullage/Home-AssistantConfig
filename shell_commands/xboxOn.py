#!/usr/bin/env python3

import socket, select, time

MY_IP_ADDRESS = '192.168.0.10'
MY_LIVE_ID = 'FD0035E9708F621E'

XBOX_PORT = 5050
XBOX_PING = "dd00000a000000000000000400000002"
XBOX_POWER = "dd02001300000010"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)
s.bind(("", 0))
s.connect((MY_IP_ADDRESS, XBOX_PORT))

live_id = MY_LIVE_ID.encode()

power_packet = bytearray.fromhex(XBOX_POWER) + live_id + b'\x00'
for i in range(0, 5):
	s.send(power_packet)
	time.sleep(1)
	
s.close()