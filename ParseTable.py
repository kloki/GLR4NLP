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

class ParseTable(object):
    """
    """
    itemSets=[]
    def __init__(self, cfg,Topsymbol):
        """
        cfg is from the CFG class
        topsymbol indicates the top class grammar most of the time "TOP"
        """
        
        #creates itemsets
        startingRules=cfg.itemRulesLHS(Topsymbol)
        self.itemSets.append(ItemSet(startingRules,cfg))



    def __str__(self):
        string=""
        for i in self.itemSets:
            string=string+ "Itemset "+str(self.itemSets.index(i))+"\n"+str(i)
        return string
    
