# ESP-NOW Header Validation

The tools in this repository can be used to show how frame headers are validated by esp-now. 

## Firmware
The Firmware receives broadcasts on channel 1.

## Setup

AirCrack and Scapy are required to run the scripts.  
Use the following command to install the dependencies on Ubuntu:  
``sudo apt install aircrack-ng python3-scapy``

First you need to create a monitoring interface:  
``sudo airmon-ng start [wireless-interface] 1``

Run the script on the monitoring interface you just created:  
``sudo ./[script].py [wireless-monitoring-interface]``

## Scripts

**invalid-fcs.py**  
Sends an ESP-NOW packet with invalid wifi fcs.  

**invalid-random-bytes.py**  
Sends an ESP-NOW packet with the random bytes always set to 0xFFFFFFFF.  

**invalid-oui.py**  
Sends an ESP-NOW packet with the oui set to 0x123456 in both the vendor specific frame and ie.  

**invalid-ie-id.py**  
Sends an ESP-NOW packet with the id of the ie set to 0xFF, which is not a vendor specific ie.  

**invalid-type-and-version.py**  
Sends an ESP-NOW packet with the type and version inside the ie set to 0x12 and 0x34.  

**combined.py**  
Sends an ESP-NOW packet with all above mentioned fields set to 0xFF.  
  
**invalid-length.py**  
Packets with a length smaller than the minimum length (5) will result in the message buffer being dumped into the receive callback.