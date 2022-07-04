import pandas as pd
import snap
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
complete_G = snap.TUNGraph.New()
for index, row in graphDF.iterrows():
    src = row['Src']
    dst = row['Dst']
    src = NameToIndexDict[src]
    dst = NameToIndexDict[dst]
    if not complete_G.IsNode(src):
        complete_G.AddNode(src)
    if not complete_G.IsNode(dst):
        complete_G.AddNode(dst)
    complete_G.AddEdge(src, dst)
    srcList.append(src)

tri_dict = {}    
for NI in complete_G.Nodes():
    NID = NI.GetId()
    if complete_G.IsEdge(NID, NID):
        complete_G.DelEdge(NID, NID)
    if NID not in tri_dict:
        tri_dict[NID] = 0
        
tStart = time.time()
#Output the number of triangles of all vertices in G
for NI in complete_G.Nodes():
    complete_G.GetNodeTriads(NI.GetId())
tEnd = time.time()
#The time spent while we set threshold=D in the graph pruning step
print( tEnd - tStart)
