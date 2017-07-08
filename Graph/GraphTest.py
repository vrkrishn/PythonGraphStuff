from Graph import TypedGraph
from StatsGraph import TypedGraphWithTrace


def TestCase():

    nodeTypeName = "nodeType"
    relatedNodeTypeName = "relatedNodeType"

    edgeTypeName = "edgeType"
    secondEdgeTypeName = "secondEdgeType"

    
    G = TypedGraphWithTrace()
    G.CreateNodeType(nodeTypeName)
    G.CreateNodeType(relatedNodeTypeName)

    G.CreateEdgeType(edgeTypeName, nodeTypeName, relatedNodeTypeName)
    G.CreateEdgeType(secondEdgeTypeName, nodeTypeName, relatedNodeTypeName)

    ### Node Upsert

    G.UpsertNode(nodeTypeName, 1)

    G.UpsertNode(nodeTypeName, 1)

    assert G.GetNodeCount(nodeTypeName) == 1

    G.UpsertNode(nodeTypeName, 2)
    G.UpsertNode(nodeTypeName, 3)
    G.UpsertNode(nodeTypeName, 4)
    G.UpsertNode(nodeTypeName, 5)

    assert G.GetNodeCount(nodeTypeName) == 5

    ### Node Get
    getNodeOutput = G.GetNodesByType(nodeTypeName)
    assert set([1,2,3,4,5]) == set([n.GetId() for n in getNodeOutput])

    ### Edge Upsert

    G.UpsertEdge(edgeTypeName, 1, 1)
    G.UpsertEdge(edgeTypeName, 2, 2)
    G.UpsertEdge(edgeTypeName, 3, 3)
    G.UpsertEdge(edgeTypeName, 4, 4)
    G.UpsertEdge(edgeTypeName, 5, 5)

    # many to many edges
    G.UpsertEdge(edgeTypeName, 4, 5)
    G.UpsertEdge(edgeTypeName, 5, 4)

    G.UpsertEdge(secondEdgeTypeName, 1, 2)
    G.UpsertEdge(secondEdgeTypeName, 2, 1)

    assert G.GetEdgeCount(edgeTypeName) == 7, "Edge Count Mismatch"
    assert G.GetNodeCount(relatedNodeTypeName) == 5, "Node Count Mismatch for type %s" %(relatedNodeTypeName)

    ### Edge Get
    getEdgeOutput = G.GetEdges()
    assert edgeTypeName in getEdgeOutput
    assert len(getEdgeOutput[edgeTypeName]) == 7
    assert secondEdgeTypeName in getEdgeOutput
    assert len(getEdgeOutput[secondEdgeTypeName]) == 2

    getEdgeByTypeOutput = G.GetEdgesByType(secondEdgeTypeName)
    assert len(getEdgeByTypeOutput) == 2

    getOutEdgesRaw = G.GetOutgoingEdges(nodeTypeName, 1)
    getOutgoingEdgesOutput = {t : [(e.GetFromId(), e.GetToId()) for e in getOutEdgesRaw[t]] for t in getOutEdgesRaw.keys()}
    assert edgeTypeName in getOutgoingEdgesOutput
    assert secondEdgeTypeName in getOutgoingEdgesOutput

    assert (1,1) in getOutgoingEdgesOutput[edgeTypeName]
    assert (1,2) in getOutgoingEdgesOutput[secondEdgeTypeName]

    getIncEdgesRaw = G.GetIncomingEdges(relatedNodeTypeName, 2)

    getIncomingEdgesOutput = {t : [(e.GetFromId(), e.GetToId()) for e in getIncEdgesRaw[t]] for t in getIncEdgesRaw.keys()}
    assert edgeTypeName in getIncomingEdgesOutput
    assert secondEdgeTypeName in getIncomingEdgesOutput

    assert (2,2) in getIncomingEdgesOutput[edgeTypeName]
    assert (1,2) in getIncomingEdgesOutput[secondEdgeTypeName]

    # Delete Edge

    G.DeleteEdge(edgeTypeName, 3, 3)
    assert G.GetNodeCount(relatedNodeTypeName) == 5
    assert G.GetNodeCount(nodeTypeName) == 5
    assert G.GetEdgeCount(edgeTypeName) == 6

    G.DeleteNode(nodeTypeName, 1)
    assert G.GetNodeCount(relatedNodeTypeName) == 5
    assert G.GetNodeCount(nodeTypeName) == 4
    assert G.GetEdgeCount(edgeTypeName) == 5
    assert G.GetEdgeCount(secondEdgeTypeName) == 1

    G.DeleteNode(relatedNodeTypeName, 1)
    assert G.GetNodeCount(relatedNodeTypeName) == 4
    assert G.GetNodeCount(nodeTypeName) == 4
    assert G.GetEdgeCount(edgeTypeName) == 5
    assert G.GetEdgeCount(secondEdgeTypeName) == 0


    # Types
    G.DeleteNodeType(nodeTypeName)
    assert not G.EdgeTypeExists(edgeTypeName)

    print G.work



if __name__ == '__main__':

    TestCase()
