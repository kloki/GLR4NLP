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
    def __init__(self,startingRules,cfg,first):
        self.items=startingRules
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
                            if follow=="$":
                                new.lookahead=current.lookahead
                                partialitems.append(new)
                            elif follow.isupper():
                                for terminal in first.getTerminals(follow):
                                    x=new
                                    x.lookahead=current.lookahead
                                    partialitems.append(x)
                            else:
                                new.lookahead=follow
                                partialitems.append(new)
                            
                            
           #remove the just extracted rule
            partialitems=partialitems[1:]

        return closure




    def __str__(self):
        string=""
        for i in self.items:
            string=string+str(i)
        return string
