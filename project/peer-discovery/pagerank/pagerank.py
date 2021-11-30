import json

def Pagerank(corpus_size, graph={}, d=0.85):
    n = len(graph)
    iter1 = {k: 1.0/corpus_size for k in graph}
    iter2 = iter1.copy()
    sinc_nodes = [i for i in graph if len(graph[i])==0]
    while True:
        sinc_nodes_contrib = sum([iter1[i]/corpus_size for i in sinc_nodes ])
        for s in graph:
            in_neighbors = [x for x in graph if s in graph[x]]
            iter2[s] = (1-d)/corpus_size + \
                d*(sum([iter1[i]/len(graph[i]) for i in in_neighbors]) + sinc_nodes_contrib)
        if sum([abs(iter2[i] - iter1[i]) for i in iter1]) < 1e-10:
            break
        iter1 = iter2.copy()
    return iter1
#with open('../crawler/crawler_result.json', 'r') as fp:
#    graph = json.load(fp)
#pagerank("pagerank_result.json", len(graph), graph, 0.85)