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
import re
sys.path.insert(0, '..') # Import the files where the modules are located

from client import PeerClient

def stop_node(node):
	if node is not None:
		node.stop()

def send_crawl():
	msg = PeerClient.msg
	msg['message'] = "crawl"
	msg['value'] = s 
	master_node.send_to_nodes(json.dumps(msg))
	done_nodes = []
	tot_nodes = master_node.get_all_connected_nodes()
	while len(done_nodes) != len(tot_nodes):
		time.sleep(5)
		for node in tot_nodes:
			if node not in done_nodes and os.path.isfile(PeerClient.output_dir + "/" + node.id + ".done"):
				done_nodes.append(node)
				print(node.id + " done")
	crawl_output = {}
	for node in done_nodes:
		with open(PeerClient.output_dir + "/" + node.id + "_crawl_output.json") as f:
			 f_output = json.loads(f)
			 for link in f_output:
			 	if link in crawl_output:
			 		crawl_output[link].extend(link)
	with open(PeerClient.output_dir + "/" + "_crawl_ouput.json", "w+") as f:
		json.dump(crawl_output, f)
	return crawl_output

# def send_pagerank():
# 	msg = PeerClient.msg
# 	msg['message'] = "pagerank"
# 	msg['value'] = s 
# 	master_node.send_to_nodes(json.dumps(msg))

	


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
			elif re.search(".txt$", s) is not None:
				

	except Exception as e:
		raise e
		stop_node(master_node)
		os._exit(1)

if __name__ == "__main__":
	main()