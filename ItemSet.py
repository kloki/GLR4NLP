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
            i=partialitems[0]
            #add extracted item to closuse
            if i not in closure:
                closure.append(i)
            #if items head non terminal extract new rules from cfg
                if i.headNonTerminal():
                    newitems=cfg.itemRulesLHS(i.head())
                #check for doubles everywhere
                    for n in newitems:
                        if (not n in closure) and (not n in partialitems):
                            partialitems.append(n)
                            partialitems[-1].lookahead="<>"
           #remove the just extracted rule
            partialitems=partialitems[1:]

        return closure




    def __str__(self):
        string=""
        for i in self.items:
            string=string+str(i)
        return string
