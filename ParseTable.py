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

from ItemSet import ItemSet
from Item import Item
from First import First


class ParseTable(object):
    """
    """
    
    

    def __init__(self):
        """
        cfg is from the CFG class
        topsymbol indicates the top class grammar most of the time "TOP"
        """
        
        pass
    
    def generateParseTable(self, cfg,topSymbol):
        """
        Creates parse table from a given grammar. 
        At the moment it is quite messy
        """
    
    
    
    
        #create First and Follow sets
        first=First(cfg,topSymbol)
        print first
        #creates itemsets
        
        #get the starting rules and set the lookahead $
        #Normally this should only be 1 TOP->S ,$
        
        startingRules=cfg.itemRulesLHS(topSymbol)
        for item in startingRules:
            item.lookahead="$"

        itemSets=[ItemSet(startingRules,cfg,first)]
        
        usedGOTOs=[startingRules[:]]
        newGOTOs=itemSets[0].getGOTOs()
        while newGOTOs!=[]:

            # get the oldest unsused Itemset, if empty break
            #create new itemsset of items generated from previous itemsets
            (newGOTO,newGOTOs)=self.getNextGOTO(newGOTOs,usedGOTOs)

            #Stop if done
            if newGOTO==[]:
                break
            #create New Item set
            itemSets.append(ItemSet(newGOTO,cfg,first))
            #add used items to used items and remove them from new items
            usedGOTOs=usedGOTOs+newGOTO
            #add the new GOTOs from the new itemset, if they will be checked later if they are already used
            newGOTOs=newGOTOs+itemSets[-1].getGOTOs()
            

        
        ##temporary printing
        self.printItemSets(itemSets)
        


    def getNextGOTO(self,newGOTOs,usedGOTOs):
        """
        Returns the highest available goto set from the stack
        """
        newGOTO=newGOTOs[0]
        newGOTOs=newGOTOs[1:]
        
        newGOTO=self.removeUsedGOTOs(newGOTO,usedGOTOs)
        if newGOTO==[]and newGOTOs!=[]:
            (newGOTO,newGOTOs)=self.getNextGOTO(newGOTOs,usedGOTOs)

        return (newGOTO,newGOTOs)
        

    def removeUsedGOTOs(self,new,used):
        """
        remove goto groups that have been used before
        """
        unused=[]
        
        for GOTO  in new:
            if GOTO not in used:
                unused.append(GOTO)
        return unused
        


    def printItemSets(self,itemSets):
        string=""
        for i in itemSets:
            string=string+ "Itemset "+str(itemSets.index(i))+"\n"+str(i)
        print string
    
