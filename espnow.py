from random import randbytes
from scapy.all import Dot11Elt
from scapy.layers.dot11 import _Dot11EltUtils, ByteField, _OUIField, IntField, StrField

ACTION_FRAME_SUBTYPE = 13
ACTION_FRAME_TYPE = 0
VENDOR_SPECIFIC_ACTION_FRAME_ID = 127
VENDOR_SPECIFIC_IE_ID = 221
ESPRESSIF_OUI = 0x18FE34
ESPNOW_TYPE = 4
ESPNOW_VERSION = 1
ESPNOW_IE_MIN_LENGTH = 5
BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"


class Dot11VendorSpecificActionFrameESP(_Dot11EltUtils):
    name = "802.11 Vendor Specific Action (Espressif ESP-NOW)"
    fields_desc = [ByteField("ID", VENDOR_SPECIFIC_ACTION_FRAME_ID),
                   _OUIField("oui", ESPRESSIF_OUI),
                   IntField("random", int.from_bytes(randbytes(4), byteorder='big'))]


class Dot11VendorSpecificIEESP(Dot11Elt):
    name = "802.11 Vendor Specific IE (Espressif ESP-NOW)"
    fields_desc = [ByteField("ID", VENDOR_SPECIFIC_IE_ID),
                   ByteField("len", ESPNOW_IE_MIN_LENGTH),
                   _OUIField("oui", ESPRESSIF_OUI),
                   ByteField("type", ESPNOW_TYPE),
                   ByteField("version", ESPNOW_VERSION),
                   StrField("data", None)]
