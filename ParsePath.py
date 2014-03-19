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

from Tree import Tree
import copy
class ParsePath(object):
    stack=[]
    nextAction=""
    loglikelihood=1

    def __init__(self,beginstate,nextAction,tree,prob):
        self.stack=beginstate
        self.nextAction=nextAction
        if tree==0:
            self.tree=Tree()
        else:
            self.tree=tree

        self.loglikelihood=prob


    def __str__(self):
        return str(self.stack)


    def getState(self):
        return self.stack[-1]

    def getTopStack(self):
        return self.stack[-1]
    
    def addAction(self,action):
        """
        It returns a clone because a path can split multiple times
        """
        return self.__class__(self.stack,action,copy.deepcopy(self.tree),self.loglikelihood)

    def reduce(self,rule):
        self.stack=self.stack[:-(len(rule.rhs)*2)]
        self.stack.append(rule.lhs)

        # update tree
        self.tree.mergeTreelets(rule.lhs,len(rule.rhs))
        
        # update loglikelihood
        self.loglikelihood+=rule.loglikelihood

        try:
            return (self.stack[-2],self.stack[-1])
        except:
            return 0 #reduce not possible something went wrong
        
    def shift(self,terminal):
        newstack=self.stack[:]
        newstack.append(terminal)
        newstack.append(int(self.nextAction[1:]))
        
        #update tree:
        self.tree.addTreelet(terminal)

        return self.__class__(newstack,"",copy.deepcopy(self.tree),self.loglikelihood)

    def goto(self,state):
        self.stack.append(state)

    
    def getTree(self):
        return self.tree.getTreeString()
