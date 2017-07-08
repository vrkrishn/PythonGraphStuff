from Graph import TypedGraph
import math


class TypedGraphWithTrace(TypedGraph):

    def __init__(self):

        super(TypedGraphWithTrace, self).__init__()
        self.stats = {}
        self.readCost = 0
        self.writeCost = 0
        self.work = 0


    # SQL Operations Cost
    def GetReadRowCost(self):
        return 1

    def GetWriteRowCost(self):
        return 1.5

    def GetSelectAllQueryPerformance(self, tableCount):
        return self.GetReadRowCost() * tableCount

    def GetSelectQueryPerformance(self, tableCount, numIndexes):
        return max(1-numIndexes, 0) * self.GetSelectAllQueryPerformance(tableCount) + numIndexes * math.log(max(1,tableCount)) * self.GetReadRowCost()

    def GetInsertIntoQueryPerformance(self, tableCount, numIndexes):
        return self.GetWriteRowCost() * (numIndexes + 1) + self.GetReadRowCost() * (numIndexes * math.log(max(1,tableCount)))

   # Overrides
    def GetNodes(self):
        for t in super(TypedGraphWithTrace, self).GetNodeTypes():
            tc = super(TypedGraphWithTrace, self).GetNodeCount(t)
            self.work += self.GetSelectQueryPerformance(tc, 0)

        return super(TypedGraphWithTrace, self).GetNodes()

    def GetNodesByType(self, typeName):
        self.work += self.GetSelectQueryPerformance(super(TypedGraphWithTrace, self).GetNodeCount(typeName),0)
        return super(TypedGraphWithTrace, self).GetNodesByType(typeName)

    def GetNodeByTypeAndId(self, typeName, nodeId):
        self.work += self.GetSelectQueryPerformance(super(TypedGraphWithTrace, self).GetNodeCount(typeName),1)
        return super(TypedGraphWithTrace, self).GetNodeByTypeAndId(typeName, nodeId)

    def GetNodeCount(self, typeName):
        return super(TypedGraphWithTrace, self).GetNodeCount(typeName)

    def GetEdgeCount(self, typeName):
        return super(TypedGraphWithTrace, self).GetEdgeCount(typeName)

    def GetEdges(self):
        for t in super(TypedGraphWithTrace, self).GetEdgeTypes():
            tc = super(TypedGraphWithTrace, self).GetEdgeCount(t)
            self.work += self.GetSelectQueryPerformance(tc, 0)

        return super(TypedGraphWithTrace, self).GetEdges()

    def GetEdgesByType(self, typeName):
        self.work += self.GetSelectQueryPerformance(super(TypedGraphWithTrace, self).GetEdgeCount(typeName),0)
        return super(TypedGraphWithTrace, self).GetEdgesByType(typeName)

    def GetOutgoingEdges(self, nodeType, nodeId):
        result = super(TypedGraphWithTrace, self).GetOutgoingEdges(nodeType, nodeId)
        for t, edges in result.iteritems():
            tc = super(TypedGraphWithTrace, self).GetEdgeCount(t)
            self.work += len(edges) * self.GetSelectQueryPerformance(tc, 1)

        return result

    def GetIncomingEdges(self, nodeType, nodeId):
        result = super(TypedGraphWithTrace, self).GetIncomingEdges(nodeType, nodeId)
        for t, edges in result.iteritems():
            tc = super(TypedGraphWithTrace, self).GetEdgeCount(t)
            self.work += len(edges) * self.GetSelectQueryPerformance(tc, 1)

        return result


    def UpsertNode(self, typename, nodeId):
        self.work += self.GetInsertIntoQueryPerformance(super(TypedGraphWithTrace, self).GetNodeCount(typename), 1)
        super(TypedGraphWithTrace, self).UpsertNode(typename, nodeId)

    def UpsertEdge(self, typename, fromId, toId):
        fromType = super(TypedGraphWithTrace, self).GetEdgeFromType(typename)
        toType = super(TypedGraphWithTrace, self).GetEdgeToType(typename)

        self.work += self.GetInsertIntoQueryPerformance(super(TypedGraphWithTrace, self).GetNodeCount(fromType), 1)
        self.work += self.GetInsertIntoQueryPerformance(super(TypedGraphWithTrace, self).GetNodeCount(toType), 1)
        self.work += self.GetInsertIntoQueryPerformance(super(TypedGraphWithTrace, self).GetNodeCount(typename), 1)

        super(TypedGraphWithTrace, self).UpsertEdge(typename, fromId, toId)



