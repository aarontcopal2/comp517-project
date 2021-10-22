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
	master_node = None

	host_ip = sys.argv[1].split(':')[0]
	host_port = int(sys.argv[1].split(':')[1])

	master_node = PeerClient(host_ip, host_port, 1, True)
	master_node.start()	

	while 1:
		s = input()
		if s == 'q' :
			stop_node(master_node)
			exit()
		elif s == 's' :
			self.send_to_nodes('{"message": "bhak lahude"}')	

except Exception as e:
	print(e)
	stop_node(master_node)
	exit()
