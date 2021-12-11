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
username = 'comp517'
password = 'comp517'
server = 'tcp:127.0.0.1;PORT=1433'
driver= '{ODBC Driver 17 for SQL Server}'
CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password

conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()


def stop_node(node):
	if node is not None:
		node.stop()

def set_master_node(master_ip):
	cursor = conn.cursor()
	query = "UPDATE leader_node SET master_ip='" + master_ip + "'"
	cursor.execute(query);
	cursor.commit()
	cursor.close()

def send_crawl(master_node, input_file):
	msg = PeerClient.msg
	msg['message'] = "crawl"

	with open(input_file) as f:
		x = [y.strip() for y in f.readlines()]

	cursor = conn.cursor()
	cursor.execute("INSERT INTO job (urls) OUTPUT Inserted.jobid values ('" + ",".join(x) + "')")
	jobid = cursor.fetchone()[0]
	conn.commit()
	msg['value'] = jobid
	master_node.send_to_all_nodes(json.dumps(msg))
	done_nodes = []
	tot_nodes = master_node.get_all_connected_nodes()
	# start of crawling time
	start_time = time.time()
	print("master peer crawling")
	master_node.crawl_started = 1
	master_node.crawl(jobid)
	print("master to peer crawling done!")
	while(False == master_node.check_if_crawl_is_done()):
		time.sleep(5)
		print("checking if nodes are done")
		
	master_node.crawl_started = 0

	crawl_output = {}

	# end of crawling time
	end_time = time.time()
	print("Time taken for crawl operation: " + str(end_time - start_time))
	print("crawling complete")
	return jobid

def send_pagerank(master_node, jobid):
	msg = PeerClient.msg
	msg['message'] = "pagerank"
	msg['value'] = jobid
	master_node.send_to_all_nodes(json.dumps(msg))
	no_done_urls = 0
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM pr_status where jobid="+str(jobid))
	tot_urls = cursor.fetchone()[0]
	cursor.close()
	master_node.pagerank(jobid)
	while no_done_urls != tot_urls:
		time.sleep(5)
		print("checking if pagerank for all urls is done")
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(*) FROM CRAWL_STATUS where jobid=" + str(jobid) + " AND status=2")
		no_done_urls = cursor.fetchone()[0]
		cursor.close()
		print(no_done_urls, "out of", tot_urls, "done")
	
	print("pagerank complete")

def main():
	master_node = None
	try:

		host_ip = "127.0.0.1"
		host_port = 8000

		set_master_node(host_ip+":"+str(host_port))

		master_node = PeerClient(host_ip, host_port, PeerClient.master_node_id, False)
		master_node.start()	

		while 1:
			s = input()
			if s == 'q' :
				stop_node(master_node)
				os._exit(1)
			elif re.search(".txt$", s) is not None:
				jobid = send_crawl(master_node, s)
				send_pagerank(master_node, jobid)

	except Exception as e:
		print("some error occurred ----------------")
		traceback.print_exc()
		stop_node(master_node)
		os._exit(1)

if __name__ == "__main__":
	main()
