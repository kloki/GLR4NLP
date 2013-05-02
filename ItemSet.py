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
from NewGoto import NewGoto


class ItemSet(object):
    """
    Collection of items for one state
    """
    items=[]
    originState=0
    state=0
    startingSymbol=0

    def __init__(self,startingRules,cfg,first,startingSymbol,originState,state):
        self.items=startingRules[:]
        self.originState=originState
        self.state=state
        self.startingSymbol=startingSymbol


        self.items=self.closure(self.items,cfg,first)


    def closure(self,partialitems,cfg,first):
        #the first terminals are determined during closure
        closure=[]
        while len(partialitems)!=0:
            #extract an item (no pop because were trying to avoid doubles)
            current=partialitems[0]
            #add extracted item to closuse
            if current not in closure:
                closure.append(current)
            #if items head non terminal extract new rules from cfg
                if current.headNonTerminal():
                    newitems=cfg.itemRulesLHS(current.head())
                #check for doubles everywhere
                    for new in newitems:
                        if (not new in closure) and (not new in partialitems):
                            follow=current.getFollowSymbol()
                            if follow=="$":#if end if item at lookahead form parrent item
                                new.lookahead=current.lookahead
                                partialitems.append(new)
                            elif follow[0].isupper():#if non terminal, get all terminals from first set
                                for terminal in first.getTerminals(follow):
                                    dup=new.dubWithLookahead(terminal)
                                    partialitems.append(dup)
                            else:#if terminal, terminal is look ahead
                                new.lookahead=follow
                                partialitems.append(new)
                            
                            
           #remove the just extracted rule
            partialitems=partialitems[1:]

        return closure

    def getGOTOs(self):
        """
        This function returns a list of tuples,
        The the tuple contains the starting symbol,list containing all items to start a new itemset.
        Their are grouped by terminal/nonterminal.
        Thus a new ItemSet needs to be generated per group
        """
        newItemsdict={}
        for item in self.items:
            if not item.itemFinished():
                new=item.pushSelf()
                newItemsdict=self.appendDict(newItemsdict,item.head(),new)
        
        newItems=[]
        for symbol,itemlist in newItemsdict.items():
            newItems.append(NewGoto(self.state,symbol,itemlist))
        return newItems

    def appendDict(self,dictionary,key,element):
        if key in dictionary:
            dictionary[key].append(element)
        else:
            dictionary[key]=[element]
        return dictionary


    def __str__(self):
        string=""
        for i in self.items:
            string=string+str(i)
        return string
