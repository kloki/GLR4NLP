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



class Rule(object):
    """
    """
    lhs=""
    rhs=[]
    probability=0
    index=0
    loglikelihood=0

    def __init__(self,lhs,rhs,probability,index ):
        """
        """
        self.lhs=lhs
        self.rhs=rhs
        self.probability=probability
        self.index=index

    def __str__(self):
        string=str(self.index)+": "+str(self.probability)[:3]+" "+self.lhs+" ->" 
        for r in self.rhs:
            string=string+" "+r
        string=string+"\n"
        return string
        
    def getLeftMost(self):
        return self.rhs[0]

    def leftMostIsTerminal(self):
        return  not self.getLeftMost()[0].isupper()


    def getFollowTuples(self):
        """
        returns a list of tuples containing Nonterminals and their follow terminal/non terminal
        """
        seq=[]

        for i in xrange(1,len(self.rhs)):
            if not self.rhs[i][0].isupper():
                seq.append((self.rhs[i-1],self.rhs[i]))
    
        return seq
