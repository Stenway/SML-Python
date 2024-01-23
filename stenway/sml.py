from stenway.reliabletxt import *
from stenway.wsv import *

class SmlNode:
	def __init__(self):
		self.whitespaces = None
		self.comment = None
	
	def _setWhitespacesAndComment(self, whitespaces, comment):
		self.whitespaces = whitespaces
		self.comment = comment
	
	def getWhitespaces(self):
		return self.whitespaces
	
	def getComment(self):
		return self.comment
	
	def toWsvLines(self, document, level, defaultIndentation, endKeyword):
		pass


class SmlEmptyNode(SmlNode):
	def __str__(self):
		super().__init__()
		return self.toString()
	
	def toString(self):
		return SmlSerializer.serializeEmptyNode2(self)
	
	def toWsvLines(self, document, level, defaultIndentation, endKeyword):
		SmlSerializer.serializeEmptyNode(self, document, level, defaultIndentation)


class SmlNamedNode(SmlNode):
	def __init__(self, name):
		super().__init__()
		self.setName(name)
	
	def setName(self, name):
		self.name = name
	
	def getName(self):
		return self.name
	
	def hasName(self, name):
		return self.name.lower() == name.lower()
	
	def toWsvLines(self, document, level, defaultIndentation, endKeyword):
		pass



class SmlAttribute(SmlNamedNode):
	def __init__(self, name, values):
		super().__init__(name)
		self.setValues(values)
	
	def setValues(self, values):
		if values == None or len(values) == 0:
			raise Exception("Values must contain at least one value")
		
		self.values = values
	
	def setValue(self, value):
		self.setValues([value])
	
	def getValues(self):
		return self.values
	
	def getString(self, index = 0):
		return self.values[index]
	
	def __str__(self):
		return self.toString()
	
	def toString(self):
		return SmlSerializer.serializeAttribute2(self)
	
	def toWsvLines(self, document, level, defaultIndentation, endKeyword):
		SmlSerializer.serializeAttribute(self, document, level, defaultIndentation)


class SmlElement(SmlNamedNode):
	def __init__(self, name):
		super().__init__(name)
		self.endWhitespaces = None
		self.endComment = None
		self.nodes = []
	
	def add(self, node):
		self.nodes.append(node)
	
	def addElement(self, name):
		element = SmlElement(name)
		self.add(element)
		return element
	
	def addAttribute(self, name, values):
		attribute = SmlAttribute(name, values)
		self.add(attribute)
		return attribute
	
	def addString(self, name, value):
		return self.addAttribute(name, [value])
	
	def getString(self, name) :
		return self.attribute(name).getValues()[0]
	
	def _setEndWhitespacesAndComment(self, whitespaces, comment):
		self.endWhitespaces = whitespaces
		self.endComment = comment
	
	def getEndWhitespaces(self):
		return self.endWhitespaces
	
	def getEndComment(self):
		return self.endComment
	
	def elements(self, name = None):
		if name != None:
			return list(filter(lambda node:(isinstance(node, SmlElement) and node.hasName(name)), self.nodes))
		else:
			return list(filter(lambda node:isinstance(node, SmlElement)), self.nodes)
	
	def hasElements(self):
		return len(self.elements()) > 0
	
	def element(self, name):
		return self.elements(name)[0]
	
	def hasElement(self, name):
		return len(self.elements(name)) > 0
	
	def attributes(self, name = None):
		if name != None:
			return list(filter(lambda node:(isinstance(node, SmlAttribute) and node.hasName(name)), self.nodes))
		else:
			return list(filter(lambda node:isinstance(node, SmlAttribute)), self.nodes)
	
	def hasAttributes(self):
		return len(self.attributes()) > 0
	
	def attribute(self, name):
		return self.attributes(name)[0]
	
	def hasAttribute(self, name):
		return len(self.attributes(name)) > 0
	
	def __str__(self):
		return self.toString()
	
	def toString(self):
		return SmlSerializer.serializeElement2(self)
	
	def toStringMinified(self):
		return SmlSerializer.serializeElementMinified(self)
	
	def toWsvLines(self, document, level, defaultIndentation, endKeyword):
		SmlSerializer.serializeElement(self, document, level, defaultIndentation, endKeyword)



class SmlDocument:
	def __init__(self, rootName = "Root"):
		self.root = SmlElement(rootName)
		self.encoding = ReliableTxtEncoding.UTF_8
		self.endKeyword = "End"
		self.defaultIndentation = None
	
		self.emptyNodesBefore = []
		self.emptyNodesAfter = []
	
	def setDefaultIndentation(self, defaultIndentation):
		if (defaultIndentation != None and len(defaultIndentation) > 0 and
				not WsvString.isWhitespace(defaultIndentation)):
			raise Exception("Indentation value contains non whitespace character")
		
		self.defaultIndentation = defaultIndentation
	
	def getDefaultIndentation(self):
		return self.defaultIndentation
	
	def setEndKeyword(self, endKeyword):
		self.endKeyword = endKeyword
	
	def getEndKeyword(self):
		return self.endKeyword
	
	def setEncoding(self, encoding):
		self.encoding = encoding
	
	def getEncoding(self):
		return self.encoding
	
	def setRoot(self, root):
		self.root = root
	
	def getRoot(self):
		return self.root
	
	def __str__(self):
		return self.toString()
	
	def toString(self):
		return SmlSerializer.serializeDocument(self)
	
	def toStringMinified(self):
		return SmlSerializer.serializeDocumentNonPreserving(self, True)
	
	def save(self, filePath):
		content = self.toString()
		file = ReliableTxtDocument(content, self.encoding)
		file.save(filePath)
	
	def parse(content):
		return SmlParser.parseDocument(content)
	
	def load(filePath):
		file = ReliableTxtDocument.load(filePath)
		content = file.getText()
		document = SmlDocument.parse(content)
		document.setEncoding(file.getEncoding())
		return document


class WsvLineIterator:	
	def hasLine(self):
		pass
	
	def isEmptyLine(self):
		pass
	
	def getLine(self):
		pass
	
	def getLineAsArray(self):
		pass
	
	def getEndKeyword(self):
		pass
	
	def getLineIndex(self):
		pass



class WsvDocumentLineIterator(WsvLineIterator):
	def __init__(self, wsvDocument, endKeyword):
		self.wsvDocument = wsvDocument
		self.endKeyword = endKeyword
		self.index = 0
	
	def getEndKeyword(self):
		return self.endKeyword
	
	def hasLine(self):
		return self.index < len(self.wsvDocument.lines)
	
	def isEmptyLine(self):
		return self.hasLine() and not self.wsvDocument.lines[self.index].hasValues()
	
	
	def getLine(self):
		line = self.wsvDocument.lines[self.index]
		self.index += 1
		return line
	
	def getLineAsArray(self):
		return self.getLine().values
	
	def getLineIndex(self):
		return self.index



class SmlParser:
	def parseDocument(content):
		wsvDocument = WsvDocument.parse(content)
		endKeyword = SmlParser.determineEndKeyword(wsvDocument)
		iterator = WsvDocumentLineIterator(wsvDocument, endKeyword)
		
		document = SmlDocument()
		document.setEndKeyword(endKeyword)
		
		document.emptyNodesBefore = SmlParser.readEmptyNodes(iterator)
		
		rootElement = SmlParser.readRootElement(iterator)
		SmlParser.readElementContent(iterator, rootElement)
		document.setRoot(rootElement)
		
		document.emptyNodesAfter = SmlParser.readEmptyNodes(iterator)
		if iterator.hasLine():
			raise SmlParser.getException(iterator, "Only one root element allowed")
		
		return document
	
	def equalIgnoreCase(name1, name2):
		if name1 == None or name2 == None:
			return name1 == name2
		
		return name1.lower() == name2.lower()
	
	def readRootElement(iterator):
		if not iterator.hasLine():
			raise SmlParser.getException(iterator, "Root element expected")
		
		rootStartLine = iterator.getLine()
		if ((not rootStartLine.hasValues()) or len(rootStartLine.values) != 1 
				or SmlParser.equalIgnoreCase(iterator.getEndKeyword(), rootStartLine.values[0])):
			raise SmlParser.getLastLineException(iterator, "Invalid root element start")
		
		rootElementName = rootStartLine.values[0]
		if rootElementName == None:
			raise SmlParser.getLastLineException(iterator, "Null value as element name is not allowed")
		
		rootElement = SmlElement(rootElementName)
		rootElement._setWhitespacesAndComment(rootStartLine.getWhitespaces(), rootStartLine.getComment())
		return rootElement
	
	def readNode(iterator, parentElement):
		node = None
		line = iterator.getLine()
		if line.hasValues():
			name = line.values[0]
			if len(line.values) == 1:
				if SmlParser.equalIgnoreCase(iterator.getEndKeyword(), name):
					parentElement._setEndWhitespacesAndComment(line.getWhitespaces(), line.getComment())
					return None
				
				if name == None:
					raise SmlParser.getLastLineException(iterator, "Null value as element name is not allowed")
				
				childElement = SmlElement(name)
				childElement._setWhitespacesAndComment(line.getWhitespaces(), line.getComment())
				
				SmlParser.readElementContent(iterator, childElement)
				
				node = childElement
			else:
				if name == None:
					raise SmlParser.getLastLineException(iterator, "Null value as attribute name is not allowed")
				
				values = line.values[1:]
				childAttribute = SmlAttribute(name, values)
				childAttribute._setWhitespacesAndComment(line.getWhitespaces(), line.getComment())
				
				node = childAttribute
		else:
			emptyNode = SmlEmptyNode()
			emptyNode._setWhitespacesAndComment(line.getWhitespaces(), line.getComment())
			
			node = emptyNode
		
		return node
	
	def readElementContent(iterator, element):
		while True:
			if not iterator.hasLine():
				raise SmlParser.getLastLineException(iterator, "Element \"" + element.getName() + "\" not closed")
			
			node = SmlParser.readNode(iterator, element)
			if node == None:
				break
			
			element.add(node)
	
	def readEmptyNodes(iterator):
		nodes = []
		while iterator.isEmptyLine():
			emptyNode = SmlParser.readEmptyNode(iterator)
			nodes.append(emptyNode)
		
		return nodes
	
	def readEmptyNode(iterator):
		line = iterator.getLine()
		emptyNode = SmlEmptyNode()
		emptyNode._setWhitespacesAndComment(line.getWhitespaces(), line.getComment())
		return emptyNode
	
	def determineEndKeyword(wsvDocument):
		for i in range(len(wsvDocument.lines)-1, 0, -1):
			values = wsvDocument.lines[i].values
			if values != None:
				if len(values) == 1:
					return values[0]
				elif len(values) > 1:
					break
		
		raise SmlParser.getParserException(len(wsvDocument.lines)-1, "End keyword could not be detected")
	
	def getParserException(line, message):
		return Exception("{} ({})".format(message, line + 1))
	
	def getException(iterator, message):
		return SmlParser.getParserException(iterator.getLineIndex(), message)
	
	def getLastLineException(iterator, message):
		return SmlParser.getParserException(iterator.getLineIndex()-1, message)


class SmlSerializer:
	def serializeDocument(document):
		wsvDocument = WsvDocument()
		
		SmlSerializer.serialzeEmptyNodes(document.emptyNodesBefore, wsvDocument)
		document.getRoot().toWsvLines(wsvDocument, 0, document.getDefaultIndentation(), document.getEndKeyword())
		SmlSerializer.serialzeEmptyNodes(document.emptyNodesAfter, wsvDocument)
		
		return wsvDocument.toString()
	
	def serializeElement2(element):
		wsvDocument = WsvDocument()
		element.toWsvLines(wsvDocument, 0, None, "End")
		return wsvDocument.toString()
	
	def serializeElementMinified(element):
		wsvDocument = WsvDocument()
		element.toWsvLines(wsvDocument, 0, "", None)
		return wsvDocument.toString()
	
	def serializeAttribute2(attribute):
		wsvDocument = WsvDocument()
		attribute.toWsvLines(wsvDocument, 0, None, None)
		return wsvDocument.toString()
	
	def serializeEmptyNode2(emptyNode):
		wsvDocument = WsvDocument()
		emptyNode.toWsvLines(wsvDocument, 0, None, None)
		return wsvDocument.toString()
	
	def serialzeEmptyNodes(emptyNodes, wsvDocument):
		for emptyNode in emptyNodes:
			emptyNode.toWsvLines(wsvDocument, 0, None, None)
	
	def serializeElement(element, wsvDocument, level, defaultIndentation, endKeyword):
		if endKeyword != None and element.hasName(endKeyword):
			raise Exception("Element name matches the end keyword '" + endKeyword + "'")
		
		childLevel = level + 1
		
		whitespaces = SmlSerializer.getWhitespaces(element.getWhitespaces(), level, defaultIndentation)
		line = WsvLine()
		line._set([element.getName()], whitespaces, element.getComment())
		wsvDocument.addLine(line)
		for child in element.nodes:
			child.toWsvLines(wsvDocument, childLevel, defaultIndentation, endKeyword)
		
		endWhitespaces = SmlSerializer.getWhitespaces(element.getEndWhitespaces(), level, defaultIndentation)
		endLine = WsvLine()
		endLine._set([endKeyword], endWhitespaces, element.getEndComment())
		wsvDocument.addLine(endLine)
	
	def getWhitespaces(whitespaces, level, defaultIndentation):
		if whitespaces != None and len(whitespaces) > 0:
			return whitespaces
		
		if defaultIndentation == None:
			indentStr = "\t" * level
			return [indentStr]
		else:
			indentStr = defaultIndentation * level
			return [indentStr]
	
	def serializeAttribute(attribute, wsvDocument, level, defaultIndentation):
		whitespaces = SmlSerializer.getWhitespaces(attribute.getWhitespaces(), level, defaultIndentation)
		combined = [attribute.getName()] + attribute.getValues()
		line = WsvLine()
		line._set(combined, whitespaces, attribute.getComment())
		wsvDocument.addLine(line)
	
	def serializeEmptyNode(emptyNode, wsvDocument, level, defaultIndentation):
		whitespaces = SmlSerializer.getWhitespaces(emptyNode.getWhitespaces(), level, defaultIndentation)
		
		line = WsvLine()
		line._set(None, whitespaces, emptyNode.getComment())
		wsvDocument.addLine(line)
	
	def serializeDocumentNonPreserving(document, minified = False):
		defaultIndentation = document.getDefaultIndentation()
		if defaultIndentation == None:
			defaultIndentation = "\t"
		
		endKeyword = document.getEndKeyword()
		if minified:
			defaultIndentation = ""
			endKeyword = None
		
		result = SmlSerializer.serializeElementNonPreserving(document.getRoot(), 0, defaultIndentation, endKeyword)
		result = result[0:-1]
		return result
	
	def serializeElementNonPreserving(element, level, defaultIndentation, endKeyword):
		result = ""
		result += SmlSerializer.getIndentationString(defaultIndentation, level)
		result += WsvSerializer.serializeValue(element.getName())
		result += "\n" 

		childLevel = level + 1
		for child in element.nodes:
			if isinstance(child, SmlElement):
				result += SmlSerializer.serializeElementNonPreserving(child, childLevel, defaultIndentation, endKeyword)
			elif isinstance(child, SmlAttribute):
				result += SmlSerializer.serializeAttributeNonPreserving(child, childLevel, defaultIndentation)
		
		result += SmlSerializer.getIndentationString(defaultIndentation, level)
		result += WsvSerializer.serializeValue(endKeyword)
		result += "\n"
		return result
	
	def serializeAttributeNonPreserving(attribute, level, defaultIndentation):
		result = ""
		result += SmlSerializer.getIndentationString(defaultIndentation, level)
		result += WsvSerializer.serializeValue(attribute.getName())
		result += " " 
		result += WsvSerializer.serializeLineValues(attribute.getValues())
		result += "\n" 
		return result
	
	def getIndentationString(defaultIndentation, level):
		return defaultIndentation * level
