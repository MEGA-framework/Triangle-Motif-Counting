import snap
import time
import pandas as pd

def algorithm(G,D, tri_dict):
    #Graph Pruning Step
    P=1
    T=0
    while P==1:
        P=0
        for NI in G.Nodes():
            NID=NI.GetId()
            d=NI.GetDeg()
            if d<=D or d>G.GetNodes()-2:
                if (d<=D and d>1) or (d>D and d>G.GetNodes()-2):
                    for i in range(d-1):
                        for j in range(i+1,d):
                            a=NI.GetNbrNId(i)
                            b=NI.GetNbrNId(j)
                            if G.IsEdge(a,b):
                                tri_dict[a] += 1
                                tri_dict[b] += 1
                                tri_dict[NID] += 1
                P=1
                G.DelNode(NID)
    #Hierarchical Clustering Step
    if G.GetNodes()>5:
        H = snap.ConvertGraph(type(G), G)
        S=[]
        i=0    
        while H.GetNodes()>0:
            S.append([])
            S[i].append(snap.GetMxDegNId(H))
            j=1
            TTT=True
            while TTT:
                s = snap.TIntV()
                snap.GetNodesAtHop(H, S[i][0], j, s, True)
                if len(s)!=0:
                    S[i].append(s)
                    j=j+1
                else:
                    TTT=False
            H.DelNode(S[i][0])
            for j in range(1,len(S[i])):
                for nodeID in S[i][j]:
                    H.DelNode(nodeID)
            i=i+1
        subgraphs = [[] for x in range(len(S))]
        #Computing Step
        for i in range(len(S)):
            for j in range(1,len(S[i])):
                G01 = G.ConvertSubGraph(snap.TUNGraph,S[i][j])
                subgraphs[i].append(G01)
            
            rootID = S[i][0]
            rootV = G.GetNI(rootID)
            d = rootV.GetDeg()
            for x in range(d-1):
                for y in range(x+1,d):
                    a=rootV.GetNbrNId(x)
                    b=rootV.GetNbrNId(y)
                    if G.IsEdge(a,b):
                        tri_dict[a] += 1
                        tri_dict[b] += 1
                        tri_dict[rootID] += 1
            G.DelNode(rootID)
        for i in range(len(S)):
            for j in range(1,len(S[i])):
                for upnodeID in S[i][j]:
                    U=[]
                    M=[]
                    for t in range(G.GetNI(upnodeID).GetDeg()):
                        a=G.GetNI(upnodeID).GetNbrNId(t)
                        if j<len(S[i])-1:
                            if subgraphs[i][j].IsNode(a):
                                U.append(a)
                        if j>1:        
                            if subgraphs[i][j-2].IsNode(a):
                                M.append(a)
                    for s in range(len(U)):
                        for t in range(s+1,len(U)):
                            if subgraphs[i][j].IsEdge(U[s],U[t]):
                                tri_dict[U[s]] += 1
                                tri_dict[U[t]] += 1
                                tri_dict[upnodeID] += 1
                    for s in range(len(M)):
                        for t in range(s+1,len(M)):
                            if subgraphs[i][j-2].IsEdge(M[s],M[t]):
                                tri_dict[M[s]] += 1
                                tri_dict[M[t]] += 1
                                tri_dict[upnodeID] += 1
        for i in range(len(S)):
            for j in range(len(S[i])-1):
                algorithm(subgraphs[i][j],D, tri_dict)
                
    return tri_dict

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
        
D = 15

tStart = time.time()
#Output the number of triangles of all vertices in G
algorithm(complete_G, D, tri_dict)
tEnd = time.time()
#The time spent while we set threshold=D in the graph pruning step
print( tEnd - tStart)