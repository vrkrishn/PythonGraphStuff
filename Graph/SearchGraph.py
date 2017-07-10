from Graph import TypedGraph

class SearchGraph(TypedGraph):

	def __init__(self):
		# We create a graph nodes and edges for type systems
		self.reservedNodeType = "__SearchGraph__TypeNode"
		self.reservedEdgeType = "__SearchGraph__TypeEdge"
		super(SearchGraph, self).CreateNodeType(self.reservedNodeType)
		super(SearchGraph, self).CreateEdgeType(self.reservedEdgeType, self.reservedNodeType, self.reservedNodeType)
	
	# Type Overrides
	def CreateNodeType(self, typeName):
		assert typeName != self.reservedNodeType, "Node Type %s reserved for search graph"%(typeName)
		super(SearchGraph, self).CreateNodeType(typeName)
		super(SearchGraph, self).UpsertNode(self.reservedNodeType, typeName, {"nodeType":typeName})
		
	def CreateEdgeType(self, typeName, fromTypename, toTypename):
        assert typename != self.reservedEdgeType, "Edge Type %s reserved for search graph"%(typeName)
        assert fromTypename != self.reservedNodeType, "Node Type %s reserved for search graph"%(fromTypeName)
        assert toTypename != self.reservedNodeType, "Node Type %s reserved for search graph"%(toTypename)	
		super(SearchGraph, self).CreateNodeType(typeName, fromTypename, toTypename)
		super(SearchGraph, self).UpsertEdge(self.reservedEdgeType, fromTypename, toTypename, {"edgeType": typeName})
		
	def DeleteEdgeType(self, typename):
		assert typename != self.reservedEdgeType, "Edge Type %s reserved for search graph"%(typeName)
        fType = super(SearchGraph, self).GetEdgeFromType(typeName)
		tType = super(SearchGraph, self).GetEdgeToType(typeName)
		super(SearchGraph, self).DeleteEdgeType(typeName)
		super(SearchGraph, self).DeleteEdge(self.reservedEdgeType, fType, tType)

    def DeleteNodeType(self, typeName):
        assert typeName != self.reservedNodeType, "Node Type %s reserved for search graph"%(typeName)
		super(SearchGraph, self).DeleteNodeType(typeName)
		super(SearchGraph, self).DeleteEdge(self.reservedNodeType, typeName)
		
	def GetNodeTypes(self):
		return [t for t in super(SearchGraph, self).GetNodeTypes() if t != self.reservedNodeType]

    def GetEdgeTypes(self):
        return [t for t in super(SearchGraph, self).GetEdgeTypes() if t != self.reservedEdgeType]

    def GetEdgeFromType(self, edgeType):
		assert edgeType != self.reservedEdgeType, "Edge Type %s reserved for search graph"%(typeName)
        return super(SearchGraph, self).GetEdgeFromType()

    def GetEdgeToType(self, edgeType):
        assert edgeType != self.reservedEdgeType, "Edge Type %s reserved for search graph"%(typeName)
        return super(SearchGraph, self).GetEdgeToType()
		
			
		
		
		
		