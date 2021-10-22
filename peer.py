#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################

import sys
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from client import PeerClient

def stop_node(node):
	if node is not None:
		node.stop()

try:
	peer_node = None

	host_ip = sys.argv[1].split(':')[0]
	host_port = int(sys.argv[1].split(':')[1])

	host_id = int(sys.argv[2])

	master_ip = sys.argv[3].split(':')[0]
	master_port = int(sys.argv[3].split(':')[1])

	peer_node = PeerClient(host_ip, host_port, host_id , True)
	peer_node.start()
	time.sleep(5)
	peer_node.connect_with_master_node(master_ip, master_port)

	while 1:
		s = input()
		if s == 'q' :
			stop_node(peer_node)
		exit()

except Exception as e:
	print(e)
	stop_node(peer_node)
	exit()