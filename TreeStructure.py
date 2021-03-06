# kloki
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Koen Klinkers k.klinkers@gmail.com

from Node import Node
from Rule import Rule

class TreeStructure(object):
    nodes={}
    bottomNodes=[]
    leftMostChains=[]
    lookaheads={}
    def __init__(self,treestring):        

        self.nodes={}
        self.bottomNodes=[]
        self.leftMostChains=[]
        self.lookahead={}

        chunks=treestring.split()

        self.nodes[0]=Node(0,chunks[0][1:],-1,[])
        parentStack=[0]
        index=1
        
        

        
        for chunk in chunks[1:]:
            
            if chunk[0]=="(":#down in tree structure
                self.nodes[index]=(Node(index,chunk[1:],parentStack[-1],[]))
                self.nodes[parentStack[-1]].addChild(index)
                parentStack.append(index)
                index+=1
                
            elif chunk[-1]==")":#up in tree structure
                chunky=chunk.split(")")
                self.nodes[index]=(Node(index,chunky[0],parentStack[-1],[]))
                self.nodes[parentStack[-1]].addChild(index)
                index+=1
                #pop parents
                parentStack=parentStack[:-(len(chunky)-1)]
            else: #stay level 
                self.nodes[index]=(Node(index,chunk,parentStack[-1],[]))
                self.nodes[parentStack[-1]].addChild(index)
                index+=1

        self.bottomNodes=[]
        for key in self.nodes:
            if self.nodes[key].children==[]:
                self.bottomNodes.append(key)

        self.leftMostChain=[]
        
        self.generateLeftMostChains()
        self.generateLookAheads() 



    
    def __str__(self):
        return self.printNode(self.nodes[0])



    def printNode(self,node):
        if len(node.children)==0:
            return node.symbol
        else:
            string="("+node.symbol
            for child in node.children:
                string+=" "+self.printNode(self.nodes[child])
            string+=")"
            return string



    def getAllSymbols(self):
        terminals=[]
        nonTerminals=[]
        for node in self.nodes.itervalues():
            if node.symbol[0].isupper():
                if node.symbol not in nonTerminals:
                    nonTerminals.append(node.symbol)
            else:
                if node.symbol not in terminals:
                    terminals.append(node.symbol)
            

        return (terminals,nonTerminals)
    


    def generateLeftMostChains(self):
        chains=[]
        for bottom in self.bottomNodes: 
            chains.append(self.getChain(self.nodes[bottom]))

        self.leftMostChains=chains


   
    def getChain(self,node):
        chain=[]

        if (node.parent !=-1 and self.isLeftChild(node)):
            
            chain=self.getChain(self.nodes[node.parent])
            
        chain.append(node)
        return chain

    def generateLookAheads(self):
        for i in xrange(len(self.bottomNodes)):
            if i+1 == len(self.bottomNodes):
                lookahead="$"
            else:
                lookahead=self.nodes[self.bottomNodes[i+1]].symbol
            self.updateLookaheadNode(self.nodes[self.bottomNodes[i]],lookahead)

    def updateLookaheadNode(self,node,symbol):
        self.lookaheads[node.index]=symbol
        if self.isRightChild(node):
            self.updateLookaheadNode(self.nodes[node.parent],symbol)



    def getLeftMostChains(self):
        return self.leftMostChains[:]

    def getTopChain(self):
        return self.leftMostChains[0]

    def getLeftMostChain(self,node):
        """
        Returns the chain with the node as highest node, if terminal the highest chain is itself
        """
        chain=[node]
        for ch in self.leftMostChains:
            if ch[0].index==node.index:
                chain=ch[:]
                break

        return chain
    

    def getLookahead(self,node):
        return self.lookaheads[node.index]
        

    def isLeftChild(self,node):
        """
        checks if node is leftest child of parent.
        """
        return node.index==self.nodes[node.parent].children[0]

    def isRightChild(self,node):
        """
        checks if node is leftest child of parent.
        """
        if node.parent==-1:
            return False
        return node.index==self.nodes[node.parent].children[-1]


    def getRightSibling(self,node):
        """
        returns right sibling of node. $ if none exist
        """
        
        if node.parent==-1 or node.index==self.nodes[node.parent].children[-1]:
            return "$"
        else:
            return self.nodes[self.nodes[node.parent].children[self.nodes[node.parent].children.index(node.index)+1]]
        

    def getSibling(self,node):
        if node=="start":
            return self.getTopNode()
        else:
            return self.getRightSibling(node)
        

    def getParentSymbol(self,node):
        return self.nodes[node.parent].symbol

    
    def getTopNode(self):
        return self.nodes[0]


    def getRule(self,parentIndex):
        """
        returns the CFG rule corresponding based on the parent node
        index and prob are still dumies values
        """
        lhs=self.nodes[parentIndex].symbol
        rhs=[]
        for i in self.nodes[parentIndex].children:
            rhs.append(self.nodes[i].symbol)
        return Rule(lhs,rhs,1,1)
        

    def getNodes(self,symbols):
        """
        This function will return al list of nodes whci match a certain state label
        """
        if symbols==[]:#beginning of tree
            return ["start"]
        if symbols==["TOP"]:
            return [self.getTopNode()]
        else:
            nodes=[]
            for parent in self.nodes.itervalues():
                if len(symbols)<=len(parent.children):
                    symbols2=[]
                    for x in xrange(len(symbols)):
                        symbols2.append(self.nodes[parent.children[x]].symbol)
                        if symbols==symbols2:
                            nodes.append(self.nodes[parent.children[len(symbols)-1]])

            return nodes


    def printLeftMostChains(self):
        for chain in self.leftMostChains:
            print self.leftMostChains.index(chain)
            for node in chain:
                print node

    # this way == and != work with this object
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)



    
