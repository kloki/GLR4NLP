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



class Item(object):
    """
    parse table item
    """
    lhs=""
    rhs=[]
    count=0
    dot=0
    lookahead="None" 
    def __init__(self,lhs,rhs,count,dot,lookahead):
        """
        """
        self.lhs=lhs
        self.rhs=rhs
        self.count=count
        self.dot=dot
        self.lookahead=lookahead
    
    def __str__(self):
        string=str(self.count)[:3]+" "+self.lhs+" ->"
        temp=self.rhs[:]
        temp.insert(self.dot,".")
        for r in temp:
            string=string+" "+r
        string=string+" , "+self.lookahead+ "\n"
        return string
    
    def symbolLeftOfDot(self):
        if self.dot==0:
            return "START"
        else:
            return self.rhs[self.dot-1]


    def head(self):
        """
        If dot at end of rule return "$"
        """
        if self.dot==len(self.rhs):
            return "$"
        else:
            return self.rhs[self.dot]


    def headNonTerminal(self):
        """
        returns True if symbols right of dot is a non terminal
        """
        if self.dot==len(self.rhs):
            return False
        else:
            return self.rhs[self.dot].isupper()
    
    def getFollowSymbol(self):
        loc=self.dot+1
        if loc==len(self.rhs):
            return "$"
        else:
            return self.rhs[loc]
        
    
    def pushSelf(self):
        """
        Returns a duplicate of itself with the dot moved on placed to right
       
        """
        return self.__class__(self.lhs,self.rhs,self.count,self.dot+1,self.lookahead)

    def dubWithLookahead(self,lookahead):
        return self.__class__(self.lhs,self.rhs,self.count,self.dot,lookahead)

    def itemFinished(self):
        """
        Checking if a new item for a new itemset needs to be generated from this item
        """
        if self.dot==len(self.rhs):
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
        
