import snap
import time

G = snap.LoadEdgeList(snap.TUNGraph, "test3.txt", 0, 1)
for NI in G.Nodes():
    NID=NI.GetId()
    if G.IsEdge(NID,NID):
        G.DelEdge(NID,NID)

tStart = time.time()
#Output the number of triangles in G
for NI in G.Nodes():
    print('%d %d' % (NI.GetId(), G.GetNodeTriads(NI.GetId())))
tEnd = time.time()
#The time spent while we set threshold=D in the pruning step
print( tEnd - tStart)