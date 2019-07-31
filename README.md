# TUN device with Python

## General info
**Tun** is virtual network device interface. It acts just like a regular interface. Except we can hook to it and control it from userspace application.
**TUN** device is used to manipulate IP packets. 
This simple program up Tun device and assign 192.168.137.1 ip address to it. Network is 192.168.137.0/28.


## REQUIREMENTS

In this project was used `standard python libraries` as well as "`_pyroute2_`" python package 

## INSTALLATION and USAGE 

`pip install pyroute2==0.4.19`

Run program 
`python tun_device.py`

Open another terminal  `ping 192.168.137.10`



