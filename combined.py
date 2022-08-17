#!/usr/bin/env python

import sys
from espnow import Dot11VendorSpecificActionFrameESP, Dot11VendorSpecificIEESP, ESPNOW_IE_MIN_LENGTH, ACTION_FRAME_SUBTYPE, ACTION_FRAME_TYPE, BROADCAST_MAC
from scapy.all import Dot11FCS, sendp, RadioTap

interface = sys.argv[1]

data_str = "this is a frame with invalid header fields\x00"
data_len = ESPNOW_IE_MIN_LENGTH+len(data_str)
packet = RadioTap() \
    / Dot11FCS(
        subtype=ACTION_FRAME_SUBTYPE,
        type=ACTION_FRAME_TYPE,
        addr1=BROADCAST_MAC,
        addr2="12:34:56:78:9a:bc",
        addr3=BROADCAST_MAC,
        FCfield=0,
        fcs=0xFFFFFFFF) \
    / Dot11VendorSpecificActionFrameESP(oui=0xFFFFFF, random=0xFFFFFFFF) \
    / Dot11VendorSpecificIEESP(ID=0xFF, oui=0xFFFFFF, len=data_len, type=0xFF, version=0xFF, data=data_str)
packet.show()
sendp(packet, iface=interface, count=1)
