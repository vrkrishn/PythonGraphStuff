class Node(object):

    def __init__(self, nodeId, typename):
        self.nodeId = nodeId
        self.typename = typename
        self.properties = {}

    def Merge(self, properties):
        self.properties.update(properties)

    def GetType(self):
        return self.typename

    def GetId(self):
        return self.nodeId

    def GetProperties(self):
        return self.properties


class Edge(object):

    def __init__(self, fromId, toId, typename):
        self.fromId = fromId
        self.toId = toId
        self.typename = typename
        self.properties = {}

    def Merge(self, properties):
        self.properties.update(properties)

    def GetType(self):
        return self.typename

    def GetFromId(self):
        return self.fromId

    def GetToId(self):
        return self.toId

    def GetProperties(self):
        return self.properties

    def __str__(self):
        return "Edge(%s->%s)"%(str(self.fromId), str(self.toId))


class NodeTable(object):
    
    def __init__(self, typename):
        self.typename = typename
        self.store = dict()
        self.count = 0

    def GetType(self):
        return self.typename

    def GetNode(self, nodeId):
        if (nodeId in self.store):
            return self.store[nodeId]
        else:
            return None

    def GetNodes(self):
        return self.store.values()

    def GetCount(self):
        return self.count


    def UpsertNode(self, nodeId, properties = {}):
        if (nodeId not in self.store):
            self.count += 1
            self.store[nodeId] = Node(nodeId, self.typename)

        self.store[nodeId].Merge(properties)

    def DeleteNode(self, nodeId):
        if (nodeId in self.store):
            self.count -= 1
            del self.store[nodeId]


class EdgeTable(object):

    def __init__(self, typeName, fromTypeName, toTypeName):
        self.fromTypeName = fromTypeName
        self.toTypeName = toTypeName
        self.typeName = typeName
        self.count = 0

        # fromId => set(toIds)
        self.fromStore = dict()
        # toId => set(fromIds)
        self.toStore = dict()

        #edge store
        self.edgeStore = dict()


    def GetType(self):
        return self.typeName

    def GetFromType(self):
        return self.fromTypeName

    def GetToType(self):
        return self.toTypeName

    def GetEdgeByFromAndToId(self, fromId, toId):
        if (fromId not in self.fromStore or toId not in self.fromStore[fromId]):
            return None
        return self.edgeStore[(fromId, toId)]

    def GetEdgesByFromId(self, fromId):
        if (fromId not in self.fromStore):
            return []
        return [self.edgeStore[(fromId, t)] for t in self.fromStore[fromId]]
    
    def GetEdgesByToId(self, toId):
        if (toId not in self.toStore):
            return []
        return [self.edgeStore[(f, toId)] for f in self.toStore[toId]]

    def GetEdges(self):
        return self.edgeStore.values()

    def GetCount(self):
        return self.count


    def UpsertEdge(self, fromId, toId, properties = {}):

        if (fromId not in self.fromStore):
            self.fromStore[fromId] = set()

        if (toId not in self.fromStore[fromId]):
            self.count += 1
            self.fromStore[fromId].add(toId)

        if (toId not in self.toStore):
            self.toStore[toId] = set()

        if (fromId not in self.toStore[toId]):
            self.toStore[toId].add(fromId)

        if ((fromId, toId) not in self.edgeStore):
            self.edgeStore[(fromId, toId)] = Edge(fromId, toId, self.typeName)

        self.edgeStore[(fromId, toId)].Merge(properties)
        

    def DeleteEdge(self, fromId, toId):

       existsEdge = self.GetEdgeByFromAndToId(fromId, toId)
       if (existsEdge is not None):
           self.count -= 1
           self.fromStore[fromId].remove(toId)
           if (len(self.fromStore[fromId]) == 0):
               del self.fromStore[fromId]

           self.toStore[toId].remove(fromId)
           if (len(self.toStore[toId]) == 0):
               del self.toStore[toId]

           del self.edgeStore[(fromId, toId)]


class TypedGraph(object):

    def __init__(self):
        # Nodes are typename => { Set(nodeId) }
        self.nodes = {}
        # Edges are typename => ( fromid => toid, toid => fromid )
        self.edges = {}


    ########## Type Management #############
    def NodeTypeExists(self, typename):
        return typename in self.nodes

    def EdgeTypeExists(self, typename):
        return typename in self.edges

    def CreateNodeType(self, typename):
        assert(typename not in self.nodes)
        self.nodes[typename] = NodeTable(typename)

    def CreateEdgeType(self, typename, fromTypename, toTypename):
        assert(typename not in self.edges)
        assert(fromTypename in self.nodes)
        assert(toTypename in self.nodes)
        self.edges[typename] = EdgeTable(typename, fromTypename, toTypename)

    def DeleteEdgeType(self, typename):
        assert(typename in self.edges)
        del self.edges[typename]


    def DeleteNodeType(self, typename):
        assert(typename in self.nodes)
        del self.nodes[typename]

        for edgeType in self.edges.values():
            if (edgeType.GetFromType() == typename or edgeType.GetToType() == typename):
                self.DeleteEdgeType(edgeType.GetType())

    def GetNodeTypes(self):
        return self.nodes.keys()

    def GetEdgeTypes(self):
        return self.edges.keys()

    def GetEdgeFromType(self, edgeType):
		assert edgeType in self.edges
        return self.edges[edgeType].GetFromType()

    def GetEdgeToType(self, edgeType):
		assert edgeType in self.edges
        return self.edges[edgeType].GetToType()


    # Read Functions
    def GetNodes(self):
        return {t : nt.GetNodes() for t,nt in self.nodes.iteritems()}

    def GetNodesByType(self, typeName):
        if (typeName not in self.nodes):
            return None
        else:
            return self.nodes[typeName].GetNodes()

    def GetNodeByTypeAndId(self, typeName, nodeId):
        if (typeName not in self.nodes):
            return None
        else:
            return self.nodes[typeName].GetNode(nodeId)

    def GetNodeCount(self, typeName):
        if (typeName not in self.nodes):
            return None
        else:
            return self.nodes[typeName].GetCount()

    def GetEdgeCount(self, typeName):
        if (typeName not in self.edges):
            return None
        else:
            return self.edges[typeName].GetCount()


    def GetEdges(self):
        return {t : et.GetEdges() for t,et in self.edges.iteritems()}

    def GetEdgesByType(self, typeName):
        if (typeName not in self.edges):
            return None
        else:
            return self.edges[typeName].GetEdges()

    def GetOutgoingEdges(self, nodeType, nodeId):
        return { t : et.GetEdgesByFromId(nodeId) for t,et in self.edges.iteritems() if et.GetFromType() == nodeType }

    def GetIncomingEdges(self, nodeType, nodeId):
        return { t : et.GetEdgesByToId(nodeId) for t,et in self.edges.iteritems() if et.GetToType() == nodeType }

    
    # Write Functions
    def UpsertNode(self, typeName, nodeId, properties = {}):
        assert typeName in self.nodes, "Have not provisioned node type"
        self.nodes[typeName].UpsertNode(nodeId, properties)

    def UpsertEdge(self, typeName, fromId, toId, properties = {}):
        assert typeName in self.edges, "Have not provisioned edge type"
        et = self.edges[typeName]

        fromType = et.GetFromType()
        toType = et.GetToType()

        self.nodes[fromType].UpsertNode(fromId)
        self.nodes[toType].UpsertNode(toId)

        et.UpsertEdge(fromId, toId, properties)


    def DeleteNode(self, typeName, nodeId):
        assert typeName in self.nodes, "Have not provisioned node type"
        
        outgoingEdges = self.GetOutgoingEdges(typeName, nodeId)
        incomingEdges = self.GetIncomingEdges(typeName, nodeId)

        for edgeType, edges in outgoingEdges.iteritems():
            for edge in edges:
                self.edges[edgeType].DeleteEdge(edge.GetFromId(), edge.GetToId())
        
        for edgeType, edges in incomingEdges.iteritems():
            for edge in edges:
                self.edges[edgeType].DeleteEdge(edge.GetFromId(), edge.GetToId())

        self.nodes[typeName].DeleteNode(nodeId)
        

    def DeleteEdge(self, typeName, fromId, toId):
        assert typeName in self.edges, "Have not provisioned edge type"
        self.edges[typeName].DeleteEdge(fromId, toId)
