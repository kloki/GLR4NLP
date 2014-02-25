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
from ParsePath import ParsePath
class Parser(object):
    
    words=[]
    categories=[]
    lookaheads=[]
    
    activePaths=[]
    shiftPaths=[]
    finishedPaths=[]
    maxNumberOfPaths=20

    def __init__(self,pt,lex):
        self.parseTable=pt
        self.lexicon=lex
        

    def parse(self, sentence):
        self.words=sentence.split()
        self.categories=self.lexicon.getCategories(self.words)
        self.lookaheads=self.categories[:]
        self.lookaheads.append("$") #add end symbol
        print self.lookaheads
        #reset
        self.activePaths=[]
        self.shiftPaths=[]
        self.finishedPaths=[]
        #start parsing
        self.activePaths.append(ParsePath([0],"none",0,0))#no tree and log likelihood 0
        while self.activePaths!=[]:
            print self.activePaths[0]
            self.reduceUntillShift()
            self.shift()
            #self.prunePaths()
        
        self.printTrees()

    def reduceUntillShift(self):
        while self.activePaths!=[]:
            path=self.activePaths.pop()
            pathActions=self.parseTable.getActions(path.getState(),self.lookaheads[0])
            
            if pathActions!=[]:#table empty, doesnt belong to grammar stop parsing    
                for action in pathActions:
                    if action=="accept":#sentence accepted
                        self.finishedPaths.append(path)
                    elif action[0]=="s":#move to shift list
                        self.shiftPaths.append(path.addAction(action))
                    elif action[0]=="r":#reduce stack and apply goto
                        newpath=path.addAction(action)
                        goto=newpath.reduce(self.parseTable.getRule(action))
                        if goto!=0:#in a proper table this will never happen. (Reduce action that is not possible)
                            newpath.goto(self.parseTable.getGOTO(goto[0],goto[1]))
                            self.activePaths.append(newpath)
                        

    def shift(self):
        terminal=self.lookaheads.pop(0)
        for path in self.shiftPaths:
            self.activePaths.append(path.shift(terminal))
        self.shiftPaths=[]

    def __str__(self):
        pass
    
    def prunePaths(self):
        rank=sorted(self.activePaths, key=lambda path: path.loglikelihood)
        self.activePaths=rank[:self.maxNumberOfPaths]


    def printpaths(self):
        print "Active"
        for i in self.activePaths:
            print i

        print "finished"

        for i in self.finishedPaths:
            print i



    def printTrees(self):
        if self.finishedPaths==[]:
            print "No parse"
        else:
            for path in self.finishedPaths:
                print str(path.loglikelihood)[:6]+" "+self.lexicalize(path.getTree())

    def lexicalize(self,tree):
        #how should I do this pretty??
        pieces=tree.split()
        wordss=self.words[:]
        ltree=""

        for piece in pieces: 
            if "(" in piece:
                ltree+=piece + " "
            elif ")" in piece:
                ltree+=piece
            else:
                treelet="("+piece.upper()+" "+wordss.pop(0)+")"
                ltree+=treelet


        
        return ltree


