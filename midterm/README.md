# Comp517 Midterm

### Introduction

You will write an introduction with the following key points
(closely related to the [Seven Key
Questions](../resources/seven-questions.pdf)). These
questions mirror the research questions you expect to pull
out of any original scholarly work. Each of these should be
approximately 1-2 paragraphs. The following sections will
provide elaboration of these elements.

* Problem + why it's important: A crawler is a program that traverses the world wide web with the purpose of indexing web pages. Search engines typically use such programs for ranking/indexing pages. The goal of this project is to create a fault-tolerant distributed web crawler.

* Research context or gap in existing approaches: Typical distributed-crawlers (Scrappy: https://doi.org/10.1088/1755-1315/108/4/042086) have master-slave configuration. Master nodes delegate the work to the slave nodes. As long as the master node is alive, the pending work of dead slave nodes can be redistributed to other active slave nodes. But if the master node dies, the entire workload is in jeopardy. Also, the client-server model creates a bottleneck on the system whereas P2P serves as a better scalable system.

* The aim/goal/hypothesis: We are proposing a peer-to-peer fault tolerant crawler since it has better fault tolerance and better scalability.

* The proposed solution: 
   * We will maintain a peer-to-peer model where a single peer would act as leader (central peer) that handles additional responsibilities related to crawling. The leader node will accept new websites from the user as input for web-crawling. 
   * Each peer will crawl upon the set of webpages assigned to it after receiving a request from master peer. The output of the crawling operation is another (larger) set of webpages. 
   * The master peer will continuously check if other crawlers have finished. Once all the peers have completed crawling, the leader node will combine results of all other nodes. It will then commence the task of Pagerank. 
   * Each peer will work on a portion of the webpage-set (output of the crawling operation) and assign a score/rank to each webpage. 

* How will you evaluate it?
   * Efficiency: We would compare performance of single-node crawler vs peer-to-peer distributed crawler to highlight the benefits of a distributed crawling approach

* Anticipated Contributions: A performant web-crawler (We believe a distributed crawler should be more performant than a serialized/single-node crawler, and a peer-to-peer crawler should have better fault-tolerance over a master-slave configuration)

### Background

**Components:**
- Peers
- Central Peer
- Crawling
- Pagerank

**Peers:**
Each peer will be a physical machine crawling a specific set of web pages. Since we are building a decentralized structured P2P network, each peer will have its own dataset for computation and will store or update the data in the central database. This database will be connected to all the peers. The distribution of this dataset will be completely dynamic and will depend on the number of peers. Each peer will receive almost an equal portion of the dataset.
A peer can receive two kinds of requests:
Crawling the web page.
Computing the pagerank for the web pages. 
Peers can come and go within a network and on any such event, the dataset would be redistributed between all the peers. Which is why, all the peers will periodically send a heartbeat message to the central peer to indicate that they are alive and working on their individual tasks. If any peer fails to send a heartbeat to the central peer, the central peer will relay a message to all peers that the peer has died and everyone would mutually agree the same and release their connections. This is essential because we are striving for a structured P2P network in which every peer has to be connected to every other peer.

**Central Peer:**
	There will be a central peer to receive requests for crawling or computing pageranks. Having a central peer saves the cost of relaying messages to every single peer. It helps us to have a single source of truth and avoids logical bugs in the network.
The responsibility of a central peer is :
- Accept the request from the user regarding the crawling of a set of websites. Each request will have its own job id.
- Add the list of web pages input by the user in the central file.
- Relay the message to all peers regarding the new request from the user.
- Send a request to all peers for computation of page rank after every user request.
- Compute its own responsibility for the request.
- Send acknowledgement for every heartbeat.
- Relay the message to all the peers that a new peer has joined and add an entry in the DB for the peer. Each peer will have its own id.  

**Crawling:**
The Internet is constantly changing and expanding. Because it is not possible to know how many total web pages there are on the Internet, the crawler will start from a seed, or a list of known URLs. The crawler will crawl the web pages at those URLs first using spiders (which is another fancy term for a physical machine crawling web pages). Each spider will have its own set of web pages that it will be crawling. As the spiders crawl those webpages, they will find hyperlinks to other URLs, and they add those to the list of pages to crawl next. Given the vast number of webpages on the Internet that could be indexed for search, this process could go on almost indefinitely. However, the web crawler will search only for a given depth in this chain of links.

**Pagerank:**
	The Pagerank score for every web page which will help us sort the highest ranked web page among a given chain of web pages. Each peer will be computing the pagerank of its set of  web pages. Since pagerank is a converging algorithm, we will start with a value and perform multiple iterations until it is about to converge.
   
   
### Proposed Approach and Evaluation Plan

We propose to complete the milestones in 2 steps:-

#### Step 1: Mid term goals and evaluation:-

**Goals**

- Implement a peer discovery mechanism so that any new node added or removed is detected and added to our pool of crawlers dynamically.
- Implement a crawler to take keywords and pages input from the “user” and scrape the web to fetch pages and links
- Implement a working page rank algorithm to run on a single node. This algorithm must be easily parallelizable so that we can extend it on other peers for Step 2.

**Evaluation**

- We will evaluate the running time of our single node page rank algorithm for a large subset of keywords and web pages
- Evaluate the time taken for peer discovery and the data bandwidth consumed.

## Grading Rubric

The proposal will be evaluated in the same way that each
research paper we read is. Key elements will include
analysis of whether the report cearly articulates:

1. the problem and its importance, 
2. related work and justifies the niche of the work, 
3. a novel hypothesis (claim about the method/idea to
   solve), 
4. a method for demonstrating the hypothesis, 
5. a feasible and strong evaluation, 

The proposal will receive equal weighting for the above
elements. I will also grad with regard to clarity of
writing, but will place less emphasis here, however, note
that to clearly describe those points you must have clear
writing.

You will also be graded on the development of your system
and results. For this deadline, I expect to see some
numbers, computation, evidence of a working systems that
does something. 
