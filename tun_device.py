import os
from fcntl import ioctl
import struct
from pyroute2 import IPRoute

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

ftun = os.open("/dev/net/tun", os.O_RDWR)
ioctl(ftun, TUNSETIFF, struct.pack("16sH", b"tun0", IFF_TUN | IFF_NO_PI))


ip = IPRoute()
idx = ip.link_lookup(ifname='tun0')[0]
ip.addr('add', index=idx, address='192.168.137.1', prefixlen=28)
ip.link('set', index=idx, state='up')
while True:
    # Read an IP packet been sent to this TUN device.
    packet = list(os.read(ftun, 2048))
    # packet = list(os.read(ftun.fileno(), 2048))

    # Modify it to an ICMP Echo Reply packet.
    #
    # Note that I have not checked content of the packet, but treat all packets
    # been sent to our TUN device as an ICMP Echo Request.

    # Swap source and destination address.
    packet[12:16], packet[16:20] = packet[16:20], packet[12:16]

    # Under Linux, the code below is not necessary to make the TUN device to
    # work. I don't know why yet, but if you run tcpdump, you can see the
    # difference.
    if True:
        # Change ICMP type code to Echo Reply (0).
        packet[20] = chr(0)
        # Clear original ICMP Checksum field.
        packet[22:24] = chr(0), chr(0)
        # Calculate new checksum.
        checksum = 0
        # for every 16-bit of the ICMP payload:
        for i in range(20, len(packet), 2):
            half_word = (ord(packet[i]) << 8) + ord(packet[i+1])
            checksum += half_word
        # Get one's complement of the checksum.
        checksum = ~(checksum + 4) & 0xffff
        # Put the new checksum back into the packet.
        packet[22] = chr(checksum >> 8)
        packet[23] = chr(checksum & ((1 << 8) -1))

    # Write the reply packet into TUN device.
    os.write(ftun, ''.join(packet))
ip.close()

