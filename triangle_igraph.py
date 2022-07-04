import pandas as pd
import igraph as ig
import time

graphDF = pd.read_csv('tweets_graph.csv', encoding = "latin-1")

allNamesList = []     
for index, row in graphDF.iterrows():
    src = row['Src']
    dst = row['Dst']
    allNamesList.append(src)
    allNamesList.append(dst)

allNamesList = list(set(allNamesList))

indexToNameDict = {}
for index, val in enumerate(allNamesList):
    indexToNameDict[index] = val

NameToIndexDict = {}
for index, val in enumerate(allNamesList):
    NameToIndexDict[val] = index

srcList = []
complete_G = ig.Graph()
complete_G.add_vertices(len(allNamesList))
edgeList = []
for index, row in graphDF.iterrows():
    src = row['Src']
    dst = row['Dst']
    src = NameToIndexDict[src]
    dst = NameToIndexDict[dst]
    edgeList.append((src, dst))
    srcList.append(src)
    
complete_G.add_edges(edgeList)
complete_G.to_undirected()
complete_G.simplify()

tStart = time.time()
complete_G.transitivity_local_undirected()
tEnd = time.time()
print( tEnd - tStart)