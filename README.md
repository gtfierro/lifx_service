## LiFX Service

Follows the UCB IoET class's advertisement service requirements. Advertises the
RPC interface over `ff02::1`, port 1525.

**Uses Python3**

### Dependencies
Install https://github.com/sharph/lifx-python 

Note: before installing lifx-python, you might need to change the BCAST address
in `lifx/network.py` if you have multiple NICs on your server.

pip packages: `sudo pip3 install twisted msgpack-python`

### How to Run

`python3 stable.py`

Sample usage is in `write.py`
