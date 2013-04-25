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
from Follow import Follow


class ParseTable(object):
    """
    """
    def __init__(self, cfg,topSymbol):
        """
        cfg is from the CFG class
        topsymbol indicates the top class grammar most of the time "TOP"
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
            #create new itemsset of items generated from previous itemsets
            itemSets.append(ItemSet(newGOTOs[0],cfg,first))
            #add used items to used items and remove them from new items
            usedGOTOs.append(newGOTOs[0])

            newGOTOs=newGOTOs[1:]
            #add the new GOTOs from the new itemset, if they not have already been used.
            potentialGOTOs=itemSets[-1].getGOTOs()
            newGOTOs=newGOTOs+self.pruneGOTOs(potentialGOTOs,usedGOTOs)
            

        
        ##temporary printing
        self.printItemSets(itemSets)
        


    def pruneGOTOs(self,new,used):
        """
        remove goto groups that have been used before
        """
        pruned=[]
        
        for n in new:
            unused=True
            for u in used:
                if n==u:
                    unused=False
                    break
            if unused:
                pruned.append(n)
        return pruned
        


    def printItemSets(self,itemSets):
        string=""
        for i in itemSets:
            string=string+ "Itemset "+str(itemSets.index(i))+"\n"+str(i)
        print string
    
