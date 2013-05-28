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

    def __init__(self):
        """
        cfg is from the CFG class
        topsymbol indicates the top class grammar most of the time "TOP"
        """
        
        pass
    
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
        
        with open(treeBank,"r") as f:
            trees=f.readlines()
            for tree in trees:
                self.generateFromTree(tree)



    def generateFromTree(self,treestring):
        tree=TreeStructure(treestring)
        print tree
                        
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
        
        tex.write("\\begin{tabular}{|l|"+"c"*numberOfTerminals+"|"+"l"*numberOfNonTerminals+"|}\n")
        tex.write("\\hline\n")
        tex.write("&\\multicolumn{"+str(numberOfTerminals)+"}{l|}{Actions} &\\multicolumn{"+str(numberOfNonTerminals)+"}{l|}{Goto}\\\\")
        tex.write("\\hline\n")
        tex.write("State")
        for key in self.actions[0].keys():
            if key =="$":
                tex.write("&\\"+key)
            else:
                tex.write("&"+key)
        for key in self.gotos[0].keys():
            tex.write("&"+key)
        tex.write("\\\\\n")        
        tex.write("\\hline\n")
        
        for state in self.actions.keys():
            tex.write(str(state))
            for symbol in self.actions[state].keys():
                tex.write("&")
                for action in self.actions[state][symbol]:
                    tex.write(action+" ")
            for symbol in self.gotos[state].keys():
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
