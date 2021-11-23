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
import json
import traceback
sys.path.insert(0, '..') # Import the files where the modules are located

from client import PeerClient

import pyodbc 
import random 

databaseName = 'master'
username = 'comp517-1'
password = 'abcd'
server = 'tcp:168.5.62.67;PORT=1433'
driver= '{SQL Server}'
CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password

conn = pyodbc.connect(CONNECTION_STRING)

cursor = conn.cursor()
cursor.execute('SELECT * FROM features')

# for i in cursor:
#     print(i)

final_crawl_output_file = PeerClient.output_dir + "/" + "_crawl_output.json"

def stop_node(node):
	if node is not None:
		node.stop()
		node.join()

def send_crawl(master_node, input_file):
	msg = PeerClient.msg
	msg['message'] = "crawl" 
	msg['value'] = input_file

	with open(input_file) as f:
		x = f.read()

	job_id = random.randrange(1,10000)
	cursor = conn.cursor()
	cursor.execute('INSERT INTO job values (' + job_id + ',"' + x + '")')
	master_node.send_to_all_nodes(json.dumps(msg))
	done_nodes = []
	tot_nodes = master_node.get_all_connected_nodes()
	# start of crawling time
	start_time = time.time()
	print("master peer crawling")
	master_node.crawl_started = 1
	master_node.crawl(input_file)
	print("master to peer crawling done!")
	while(False == master_node.check_if_crawl_is_done()):
		time.sleep(5)
		
	master_node.crawl_started = 0

	crawl_output = {}

	# end of crawling time
	end_time = time.time()
	print("Time taken for crawl operation: " + str(end_time - start_time))
	done_nodes.append(master_node.node)
	for node in done_nodes:
		with open(PeerClient.output_dir + "/" + node.id + "_crawl_output.json") as f:
			 f_output = json.loads(f.read())
			 for (link, outlinks) in f_output.items():
			 	if link in crawl_output:
			 		crawl_output[link].extend(outlinks)
			 	else :
			 		crawl_output[link] = outlinks
	
	with open(final_crawl_output_file, "w+") as f:
		json.dump(crawl_output, f)
	print("crawling complete")
	return final_crawl_output_file

def send_pagerank(master_node, input_file):
	msg = PeerClient.msg
	msg['message'] = "pagerank"
	msg['value'] = input_file 
	master_node.send_to_all_nodes(json.dumps(msg))
	done_nodes = []
	tot_nodes = master_node.get_all_connected_nodes()
	master_node.pagerank(input_file)
	while len(done_nodes) != len(tot_nodes):
		time.sleep(5)
		print("checking if pagerank for nodes are done")
		for node in tot_nodes:
			if node not in done_nodes and os.path.isfile(PeerClient.output_dir + "/" + node.id + ".done"):
				done_nodes.append(node)
				print(node.id + " done")
				
	pagerank_output = {}
	done_nodes.append(master_node.node)
	for node in done_nodes:
		with open(PeerClient.output_dir + "/" + node.id + "_pagerank_output") as f:
			 f_output = json.loads(f.read())
			 for (link, pagerank) in f_output.items():
			 	if link in pagerank_output:
			 		pagerank_output[link] += pagerank
			 	else :
			 		pagerank_output[link] = pagerank
	
	with open(PeerClient.output_dir + "/" + "_pagerank_ouput", "w+") as f:
		json.dump(pagerank_output, f)
	
	print("pagerank complete")

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
				final_crawl_output_file = send_crawl(master_node, s)
				send_pagerank(master_node, final_crawl_output_file)

	except Exception as e:
		print("some error occurred ----------------")
		traceback.print_exception()
		stop_node(master_node)
		os._exit(1)

if __name__ == "__main__":
	main()
