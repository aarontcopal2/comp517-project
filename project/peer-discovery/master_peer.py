#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################

import sys
import os
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from client import PeerClient

def stop_node(node):
	if node is not None:
		node.stop()

def main():
	master_node = None
	try:

		# host_ip = sys.argv[1].split(':')[0]
		# host_port = int(sys.argv[1].split(':')[1])

		host_ip = "127.0.0.1"
		host_port = 8000

		master_node = PeerClient(host_ip, host_port, PeerClient.master_node_id, True)
		master_node.start()	

		while 1:
			s = input()
			if s == 'q' :
				stop_node(master_node)
			os._exit(1)
			# elif len(s)>1 and s[0] == 's' :
			# 	msg = PeerClient.msg
			# 	msg['message'] = "from_master"
			# 	msg['value'] = s[2:] 
			# 	self.send_to_nodes(json.dumps(x))	

	except Exception as e:
		raise e
		stop_node(master_node)
		os._exit(1)

if __name__ == "__main__":
	main()