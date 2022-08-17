#!/usr/bin/env python

import sys
from espnow import Dot11VendorSpecificActionFrameESP, Dot11VendorSpecificIEESP, ESPNOW_IE_MIN_LENGTH, ACTION_FRAME_SUBTYPE, ACTION_FRAME_TYPE, BROADCAST_MAC
from scapy.all import Dot11FCS, sendp, RadioTap

interface = sys.argv[1]

packet = RadioTap() \
    / Dot11FCS(
        subtype=ACTION_FRAME_SUBTYPE,
        type=ACTION_FRAME_TYPE,
        addr1=BROADCAST_MAC,
        addr2="12:34:56:78:9a:bc",
        addr3=BROADCAST_MAC,
        FCfield=0) \
    / Dot11VendorSpecificActionFrameESP() \
    / Dot11VendorSpecificIEESP(len=4)
packet.show()
sendp(packet, iface=interface, count=1)
