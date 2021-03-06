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
    originItems=[]
    state=0
    symbol=""
    def __init__(self,startingRules,cfg,first,symbol,state):
        self.items=startingRules[:]
        self.originItems=startingRules[:]
        self.state=state
        self.symbol=symbol

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
                            if follow=="$":#if at the end of rule is lookahead of parent
                                new.lookahead=current.lookahead
                                partialitems.append(new)
                            else:
                                for terminal in first.getTerminals(follow):
                                    dup=new.dubWithLookahead(terminal)
                                    partialitems.append(dup)
                            
                            
           #remove the just extracted rule
            partialitems=partialitems[1:]

        return closure

    def getGOTOs(self):
        """
        This function returns a list of tuples,
        The the tuple contains the starting symbol,lookahead,list containing all items to start a new itemset.
        Their are grouped by terminal/nonterminal.
        Thus a new ItemSet needs to be generated per group
        """
        newItemsdict={}
        for item in self.items:
            if not item.itemFinished():
                new=item.pushSelf()
                newItemsdict=self.appendDict(newItemsdict,item.head(),new)
       
        #Ordering Nonterminals before terminals for readability
        newItems1=[]
        newItems2=[]
        for symbol,itemlist in newItemsdict.items():
            if symbol[0].isupper():
                newItems1.append(NewGoto(self.state,symbol,itemlist))
            else:
                newItems2.append(NewGoto(self.state,symbol,itemlist))
            
        return newItems1+newItems2


    def update(self,items,cfg,first):
        new=[]
        
        for i in items:
            if i not in self.originItems:
                self.originItems.append(i)
                new.append(i)
        
        for newI in self.closure(new,cfg,first):
            if newI not in self.items:
                self.items.append(newI)
        
        


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

    def stringItems(self,items):
        string=""
        for i in items:
            string=string+str(i)
        return string
