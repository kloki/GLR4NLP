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
from Item import Item
class ItemSet(object):
    """
    Collection of items for one state
    """
    items=[]
    def __init__(self,startingRules,cfg):
        self.items=startingRules
        (self.items,self.first)=self.closure(self.items,cfg)
        


    def closure(self,partialitems,cfg):
        #the first terminals are determined during closure
        closure=[]
        first=First()
        while len(partialitems)!=0:
            #extract an item (no pop because were trying to avoid doubles)
            i=partialitems[0]
            #add extracted item to cluse
            if i not in closure:
                closure.append(i)
            #if items head non terminal extract new rules from cfg
                if i.headNonTerminal():
                    newitems=cfg.itemRulesLHS(i.head())
                #check for doubles everywhere
                    for n in newitems:
                        if (not n in closure) and (not n in partialitems):
                            partialitems.append(n)
           #remove the just extracted list
            partialitems=partialitems[1:]

        return (closure,first)


    def getLHS(self,items):
        """
        Needed for adding the starting rules terminal to the first set
        to determine follow set. Net pretty
        """
        LHSs=[]
        for item in items:
            LHSs.append(item.lhs)

        return LHSs
    
    def setLookAheads(self, items,follow):
        LAitems=[]
        for item in items:
            for lookahead in follow.getLookaheads(item.lhs):
                LAitems.append(item.spawnWithLookahead(lookahead))

        return LAitems

    def __str__(self):
        string=""
        for i in self.items:
            string=string+str(i)
        return string
