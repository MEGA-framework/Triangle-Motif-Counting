import networkit as nk
import pandas as pd
import networkx as nx
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
complete_G = nx.Graph()
for index, row in graphDF.iterrows():
    src = row['Src']
    dst = row['Dst']
    src = NameToIndexDict[src]
    dst = NameToIndexDict[dst]
    complete_G.add_edge(src, dst)
    srcList.append(src)
    
for NID in complete_G:
    if complete_G.has_edge(NID, NID):
        complete_G.remove_edge(NID, NID)
        
complete_G = nk.nxadapter.nx2nk(complete_G)

tStart = time.time()
cc = nk.centrality.LocalClusteringCoefficient(complete_G)
cc.run()
tEnd = time.time()
print( tEnd - tStart)