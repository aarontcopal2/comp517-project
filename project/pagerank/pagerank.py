def pagerank(corpus_size, graph={}, d=0.85):
    n = len(graph)
    iter1 = [1.0/corpus_size]*corpus_size
    iter2 = iter1[:]
    sinc_nodes = [i for i in graph if len(graph[i])==0]
    while True:
        sinc_nodes_contrib = sum([iter1[i]/corpus_size for i in sinc_nodes ])
        for s in graph:
            in_neighbors = [x for x in graph if s in graph[x]]
            iter2[s] = (1-d)/corpus_size + \
                d*(sum([iter1[i]/len(graph[i]) for i in in_neighbors]) + sinc_nodes_contrib)
        if sum([abs(iter2[i] - iter1[i]) for i in range(len(iter1))]) < 1e-10:
            break
        iter1, iter2 = iter2, iter1
    return iter1


graph = {0:[1], 1:[2], 2:[0]}

pagerank(3, graph, 0.85)





