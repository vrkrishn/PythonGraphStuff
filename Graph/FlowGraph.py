from Graph import TypedGraph

class FlowGraph(TypedGraph):

	def __init__(self):
		# Flow Node Types
		self.nodeTypeName = "Node"
		self.CreateNodeType(self.nodeTypeName)
		
		# Flow Edge Types
		self.edgeTypeName = "NodeToNode"
		self.CreateEdgeType(self.edgeTypeName, self.nodeTypeName, self.nodeTypeName)

		self.nodeIds = set()
		
    def UpsertNode(self, nodeId):
		assert (nodeId not in self.nodeIds)
		super(FlowGraph,self).UpsertNode(self.nodeTypeName, nodeId, {"nodeType": "Node"})
		
	def UpsertSource(self, nodeId):
		assert (nodeId not in self.nodeIds)
		super(FlowGraph,self).UpsertNode(self.nodeTypeName, nodeId, {"nodeType": "Source"})
		
	def UpsertTarget(self, nodeId):
		assert (nodeId not in self.nodeIds)
		super(FlowGraph,self).UpsertNode(self.nodeTypeName, nodeId, {"nodeType": "Target"})
	
    def UpsertEdge(self, typeName, fromId, toId, weight):
        super(FlowGraph,self).UpsertEdge(typeName, fromId, toId, {"weight":weight})
		
		
	def SingleSourceSingleTargetMaximumFlow(self, sourceId, targetId):
		# make sure that the source and target ids are of the right type
		sourceNode = super(FlowGraph, self).GetNode(self.nodeTypeName, sourceId)
		assert(sourceNode.GetProperties()["nodeType"] == "Source")
		
		targetNode = super(FlowGraph, self).GetNode(self.nodeTypeName, targetId)
		assert(sourceNode.GetProperties()["nodeType"] == "Target")
		
		
		
	

