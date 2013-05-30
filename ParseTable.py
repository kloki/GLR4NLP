#!/usr/bin/env python
#
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


import cPickle as pickle
import os
from ItemSet import ItemSet
from Item import Item
from First import First
from TreeStructure import TreeStructure

class ParseTable(object):
    """
    action stores all actions
    gotos stores all gotos
    rules stores all grammar rules indexed on index number
    """


    actions={}
    gotos={}
    rules={}
    stateLabels={}
    rulesList=[]
    def __init__(self):
        """
        cfg is from the CFG class
        topsymbol indicates the top class grammar most of the time "TOP"
        """
        
        
    
    def generateFromGrammar(self, cfg,topSymbol):
        """
        Creates parse table from a given grammar. 
        At the moment it is quite messy
        """

    
        ###########ITEMSETS#####################
    
        #create First set
        first=First(cfg,topSymbol)
        print first
        #creates itemsets
        
        #get the starting rules and set the lookahead $
        #Normally this should only be 1 TOP->S ,$
        
        startingRules=cfg.itemRulesLHS(topSymbol)
        for item in startingRules:
            item.lookahead="$"

        #initialize first ItemSet
        itemSets=[ItemSet(startingRules,cfg,first,topSymbol,0)]
        
        
        #now expand untill done
        newGOTOs=itemSets[0].getGOTOs()
        statecounter=1
        itemSetRelations=[]
        
        while newGOTOs!=[]:
            newGOTO=newGOTOs.pop(0)

            
            #check if goto is already used
            used=False
            for itemset in itemSets:
                for item in newGOTO.items:
                    if item in itemset.originItems:
                        used=True
                        #add relation
                        itemSetRelations.append((newGOTO.originState,newGOTO.symbol,itemset.state))
                        #update Itemset, mostly new look ahead symbols will emerge for old items
                        oldGOTOs=itemset.getGOTOs()
                        itemset.update(newGOTO.items,cfg,first)
                        #but them in newGOTO as new items will cascade through old itemsets
                        potentialGOTOs=itemset.getGOTOs()
                        if len(potentialGOTOs)!=len(oldGOTOs):
                            newGOTOs=newGOTOs+potentialGOTOs
                        break
                if used:#double break
                    break

            if used ==False:
                
            #create New Item set
                itemSets.append(ItemSet(newGOTO.items,cfg,first,newGOTO.symbol,statecounter))
                
            
                #save itemset relations
                itemSetRelations.append((newGOTO.originState,newGOTO.symbol,statecounter))
                statecounter+=1
                #get the new GOTOs from the newest itemset, they will be checked later if they are already used
                newGOTOs=newGOTOs+itemSets[-1].getGOTOs()
            

        
        ##temporary printing
        self.printItemSets(itemSets)
        print itemSetRelations
        ###############PARSETABLE###################

        #store all rules from cfg

        for rule in cfg.listAllRules():
            self.rules[rule.index]=rule

        #setup parsetable data structure
        terminals=cfg.getAllTerminals()
        nonTerminals=cfg.getAllNonTerminals()
        for i in xrange(len(itemSets)):
            self.actions[i]={}
            self.gotos[i]={}

            for t in terminals:
                self.actions[i][t]=[]
            self.actions[i]["$"]=[]#add endsymbol

            for nt in nonTerminals:
        
                self.gotos[i][nt]=[]
        #fill parsetable
        #GOTO table
                
        shiftstates={}
        for i in itemSets:
            shiftstates[i.state]={}
            for t in terminals:
                shiftstates[i.state][t]=[]
        
        for i in itemSetRelations:
            if i[1] in nonTerminals:
                self.gotos[i[0]][i[1]].append(i[2])
                
            else:
                if i[2] not in shiftstates[i[0]][i[1]]:
                    shiftstates[i[0]][i[1]].append(i[2])
        #action table
        for itemset in itemSets:
            for item in itemset.items:
                if item.headTerminal():
                    #retrieve shift states:
                    for shift in shiftstates[itemset.state][item.head()]:
                        if ("s"+str(shift)) not in self.actions[itemset.state][item.head()]:
                            self.actions[itemset.state][item.head()].append(("s"+str(shift)))
                elif(item.lhs==topSymbol and item.itemFinished() and item.lookahead=="$"):
                    if "accept" not in self.actions[itemset.state]["$"]:
                        self.actions[itemset.state]["$"].append("accept")
                elif(item.itemFinished()):
                    if ("r"+str(item.index)) not in self.actions[itemset.state][item.lookahead]:
                        self.actions[itemset.state][item.lookahead].append("r"+str(item.index))
        



    def generateFromTreeBank(self,treeBank):
        
        #bit of juggling with data structures
        self.rulesList=[]
        for rule in self.rules.itervalues():
            self.rulesList.appendRule
        

        with open(treeBank,"r") as f:
            trees=f.readlines()
            for tree in trees[:1]:
                self.generateFromTree(tree)


        self.rules={}
        for rule in self.rulesList:
            self.rules[rule.index]=rule

        self.rulesList=[]

    def addAction(self,dic,state,symbol,action):
        if action not in dic[state][symbol]:
            dic[state][symbol].append(action)


    def generateFromTree(self,treestring):
        

        tree=TreeStructure(treestring)
        self.updateTableSymbols(tree.getAllSymbols())
        


        todo=["start"]
        state2chain={}
        state2chain["start"]=tree.getTopChain()


        while todo!=[]:
            #print todo
            #get action
            currentState=todo.pop(0)
            #get current state
            state=self.stateLabels[currentState]
            print "NEWTODO"
            print currentState
            print state
            if currentState=="start":
                currentChain=tree.getTopChain()
                for node in currentChain:
                    #check if exists
                    if node.symbol not in self.stateLabels.keys():
                        self.createState(node.symbol)
                        state2chain[node.symbol]=currentChain
                    if node.symbol[0].isupper():
                        self.addAction(self.gotos,state,node.symbol,self.stateLabels[node.symbol])    
                    else:
                        self.addAction(self.actions,state,node.symbol,("s"+str(self.stateLabels[node.symbol])))
                    todo.append(node.symbol)
            else:
                #get all the siblings belonging to this state and its corresponding chain, Note siblings by definition don't belong to the current state
                siblings=[]
                currentNodes=[]
                symbol=currentState.split()[-1]
                
                for node in state2chain[currentState]:
                    if node.symbol==symbol:
                        siblings.append(tree.getRightSibling(node))
                        currentNodes.append(node)
              #get look ahead
                lookahead=tree.getLookahead(state2chain[currentState][-1])
                for i in xrange(len(siblings)):
                    sibling=siblings[i]
                    currentNode=currentNodes[i]
                    if sibling=="$":
                        if currentState=="TOP":
                            self.addAction(self.actions,state,"$","accept")
                        else:
                            index=self.getIndex(tree.getRule(currentNode.parent))
                            self.addAction(self.actions,state,tree.getLookaheadNode(currentNode),("r"+str(index)))
                    elif sibling.symbol[0].isupper():
                        #get the chain with the current node as top
                        currentChain=tree.getLeftMostChainHead(sibling)
                        for node in currentChain:
                            if node.symbol[0].isupper():
                                newstate=currentState+" "+node.symbol
                                if newstate not in self.stateLabels.keys():
                                    self.createState(newstate)
                                    state2chain[newstate]=currentChain
                                self.addAction(self.gotos,state,node.symbol,self.stateLabels[newstate])    
                                todo.append(newstate)
                            else:
                                if node.symbol not in self.stateLabels.keys():
                                    self.createState(node.symbol) 
                                    state2chain[node.symbol]=currentChain
                                self.addAction(self.actions,state,node.symbol,("s"+str(self.stateLabels[node.symbol])))
                                todo.append(node.symbol)
                    else:#sybling is terminal, the same as sybling is lookahead. 
                        newstate=currentState+" "+sibling.symbol
                        if newstate not in self.stateLabels.keys():
                            self.createState(newstate)
                            #because were dealing with terminals we can easily determine the new chain, the next one
                            state2chain[newstate]=tree.getNextChain(state2chain[currentState])
                        self.addAction(self.actions,state,sibling.symbol,("s"+str(self.stateLabels[newstate])))
                        todo.append(newstate)

    def createState(self,name):
        self.stateLabels[name]=len(self.actions.keys())
        self.actions[self.stateLabels[name]]={}
        self.gotos[self.stateLabels[name]]={}
        for i in self.actions[0].keys():
            self.actions[self.stateLabels[name]][i]=[]
        
        for i in self.gotos[0].keys():
            self.gotos[self.stateLabels[name]][i]=[]


    def getIndex(self,rule):
        index=0
        present=False
        for i in self.rulesList:
            if i.lhs==rule.lhs and i.rhs==rule.rhs:
                index=i.index
                present=True
        if not present:
            rule.index=len(self.rulesList)
            self.rulesList.append(rule)
            index=rule.index
        return index


    def updateTableSymbols(self,symbols):
        terminals=symbols[0]
        nonTerminals=symbols[1]
        if self.actions=={}:#empty table
            self.actions[0]={}
            self.gotos[0]={}
            self.stateLabels["start"]=0
            for terminal in terminals:
                self.actions[0][terminal]=[]
            self.actions[0]["$"]=[]
            for nonTerminal in nonTerminals:
                self.gotos[0][nonTerminal]=[]


        else:
            terminals=set(terminals).difference(set(self.actions[0].keys()))
            nonTerminals=set(nonTerminals).difference(set(self.gotos[0].keys()))
            for  state in self.actions:
                for terminal in terminals:
                    self.actions[state][terminal]=[]
            for state in self.gotos:
                for nonTerminal in nonTerminals:
                    self.gotos[state][nonTerminal]=[]




    def printItemSets(self,itemSets):
        string=""
        for i in itemSets:
            string=string+ "Itemset "+str(itemSets.index(i))+"\n"+str(i)
        print string
    

    def __str__(self):

        string=""

        string+="ACTION TABLE\n"
        for i in self.actions.iterkeys():
            for j in self.actions[i].iterkeys():
                if self.actions[i][j]!=[]:
                    for k in self.actions[i][j]:
                        string+="ACTION("+str(i)+","+j+")="+k+"\n"

        string+="\nGOTO TABLE\n"
        for i in self.gotos.iterkeys():
            for j in self.gotos[i].iterkeys():
                if self.gotos[i][j]!=[]:
                    for k in self.gotos[i][j]:
                        string+="GOTO("+str(i)+","+j+")="+str(k)+"\n"

        return string

    def save(self,filename):
        pickle.dump( (self.actions,self.gotos,self.rules), open( filename+".pt", "wb" ) )


    def load(self,filename):
        (self.actions,self.gotos,self.rules) = pickle.load( open( filename+".pt", "rb" ) )


    def texfile(self,PDF):
        """
        This creates a tex file with the parse table.
        If PDF is true the tex file is converted to a PDF. Only works on unix 
        """
        tex=open("parsetable.tex","w")
        tex.write("\\documentclass[11pt]{article}\n")
        tex.write("\\title{ParseTable}\n")
        tex.write("\\begin{document}\n")
        tex.write("\\maketitle\n")
        numberOfTerminals=len(self.actions[0])
        numberOfNonTerminals=len(self.gotos[0])
        numberOfStats=len(self.actions)
        
        tex.write("\\begin{tabular}{|l|l|"+"c"*numberOfTerminals+"|"+"l"*numberOfNonTerminals+"|}\n")
        tex.write("\\hline\n")
        tex.write("&&\\multicolumn{"+str(numberOfTerminals)+"}{l|}{Actions} &\\multicolumn{"+str(numberOfNonTerminals)+"}{l|}{Goto}\\\\")
        tex.write("\\hline\n")
        tex.write("&State")
        terminals=self.actions[0].keys()
        nonTerminals=self.gotos[0].keys()


        for key in terminals:
            if key =="$":
                tex.write("&\\"+key)
            else:
                tex.write("&"+key)
        for key in nonTerminals:
            tex.write("&"+key)
        tex.write("\\\\\n")        
        tex.write("\\hline\n")
        
        inverseStates={}
        for name,state in self.stateLabels.iteritems():
            inverseStates[state]=name
        
        for state in self.actions.keys():
            
            tex.write(inverseStates[state])
            tex.write("&")
            tex.write(str(state))
            for symbol in terminals:
                tex.write("&")
                for action in self.actions[state][symbol]:
                    tex.write(action+" ")
            for symbol in nonTerminals:
                tex.write("&")
                for goto in self.gotos[state][symbol]:
                    tex.write(str(goto)+" ")
            tex.write("\\\\\n")




        tex.write("\\hline\n")
        tex.write("\\end{tabular}\n")
        tex.write("\\end{document}\n")
        tex.close()

        if PDF:
            os.system("pdflatex parsetable.tex >/dev/null")
            os.system("rm parsetable.aux parsetable.log")

    def getActions(self,state,lookahead):
        return self.actions[state][lookahead]

    def getGOTO(self,state,nonTerminal):
        return self.gotos[state][nonTerminal][0]#for now i am assumming there can be only one goto state

    def getRule(self,index):
        return self.rules[int(index[1:])]
