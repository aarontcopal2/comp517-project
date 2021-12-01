# Comp517 Project Hacking

You will identify and contribute to the understanding and
knowledge on a problem related to operating systems. It is
anticipated that this project will identify a compelling and
technically interesting problem and make concrete progress
towards solving that problem. The project must emphasize
original contributions to the conversation on the topic and
result in a real software artifacts as well as evidence to
support the hypothesis for how to solve the problem. You
will sketch out the problem, related literature, and plan in
the [project proposal](../proposal/README.md) and execute
its plan with code located in this directory. 

The primary objective of this project is to make a
hypothesis for addressing a current problem. A project will
typically take one of two forms: 1) system that includes
novel design and implementation elements to address the gap
in the literature or 2) devises a hypothesis and explores a
concrete phenomena of interest in an empirical
investigation. 

## Grading

Grading projects is hard to define in general, however, it
is anticipated that you will produce code that I can run and
test out. That you will generate artifacts demonstrating
that your idea does in fact address the problem you propose
and is distinct from related work. It need not be successful
in producing better results, but we should learn something
from the investigation. It is anticipated that at the
[midterm report](../midterm/README.md) you will a running
prototype that you can demo. For the final we anticipate an
independent project that can be run by the professor.


## How to run it

1. Create the database tables using the DDL file 
`DDL_SQL_QUERY.txt`

2. Move to the main directory
`cd peer-discovery`

3. Start a master peer using the script
`python master_peer.py`

4. Start a peer using the script peer.py. Pass the ip_address:port and node id. Eg: 
`python peer.py 127.0.0.1:8001 2`

    (The peer you just started will connect with master peer and exchange messages)

5. After master and peer nodes establish connection, you can start to send crawl requests to master peer. Type in
`input.txt`
    to the master peer to send a crawl request. You should already have list of urls in the input.txt file and the master peer will send this info to all connected peers
    
6. Watch the magic happen. The master peer will add the job id to the database and the latest job id is the one used for crawl which you can find in the `job` table. Crawl status for every node and url can be found in the `crawl_status` table. If it is 1 then the crawl has started and if 2 then the status is complete. The `graph` table stores the url and the crawled linked webpages which are comma separated. It also has the nodeid to describe which node crawled the url.

7. Try to disconnect one node by exiting the process or typing in `q` for a peer which is not master. As soon as you disconnect, if any node is yet to finish its work, it will recalculate the work and add the urls of the exited node to its list. To confirm, you may check the nodeid attribute in the `crawl_status` table for the url which should be flipped to the node id which accepted the additional work. 


8. Try to add a node to the network, make sure that the rest of the nodes haven't finished their crawling. As soon as the initial set of messages are interchanged between master and new node, the master peer will send an additional request to crawl if the crawl hasn't finished. The new node starts its crawling. Here, you can also check the debug statements printed out for every url added to the `graph` table which says `Finished writing 1 url to db`. The new node should be printing these. You can check the `graph` table and the `crawl_status` tables to get details about what all urls were crawled by the new node.
 
9. After the crawling is done, the master peer will then shoot a request for pagerank. The nodes find their subset of urls and compute the pagerank. We can find the pagerank info in the `pagerank` and the intermediate status in the `pagerank_status` tables.

## Evaluation
For performance evaluation, we need to evaluate the components/algorthms of our system (the components implemented for midterm): crawler and pagerank

##### Execution results of crawler

| # input urls | # nodes | Search depth | Time (sec) |
|--------------|---------|--------------|------------|
| 2            | 1       | 2            | 49.82      |
| 2            | 2       | 2            | 30.51      |
| 2            | 1       | 3            | 733.52     |
| 2            | 2       | 3            | 249.48     |

P.S: The two urls used as input were https://www.rice.edu, https://www.stackoverflow.com


##### Execution results of pagerank
The pagerank implementation that we use has good performance and completes instantaneously. Thus we find that its needless to evaluate the execution time of pagerank.
