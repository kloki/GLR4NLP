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

import cPickle as pickle

class Lexicon(object):
    """
    extracts the lexical words from tree bank and stores them.
    """
    def __init__(self,treebankName,path):

        
        f=open(treebankName,"r")
        treebank=f.read()
        f.close()

        #some sanitizing
        treebank=treebank.replace(" (, ,)","")
        treebank=treebank.replace(" (. .)","")
        treebank=treebank.replace(" (. ?)","")
        treebank=treebank.replace(" (. !)","")
        treebank=treebank.replace(" (\" \")","")
        treebank=treebank.replace(" (' ')","")
        treebank=treebank.replace(" ('' '')","")
        treebank=treebank.replace(" (`` ``)","")
        treebank=treebank.replace(" (; ;)","")
        treebank=treebank.replace(" (: :)","")
        treebank=treebank.replace(" (-LRB- -LRB-)","")
        treebank=treebank.replace(" (-RRB- -RRB-)","")
        treebank=treebank.replace(") )","))")


        #extract the terminals
        index=0
        trees=treebank.split("\n")
        outputTrees=open(path+"treebank","w")
        transform={}
        for tree in trees:
            words=tree.split()
            transform[index]=[]
            for i in xrange(len(words)):
                
                if ")" in words[i]:
                    (lb,nonterminal)=self.breakup(words[i-1],"(")
                    (terminal,rb)=self.breakup(words[i],")")
                    nonterminal2=nonterminal.lower()
                    words[i-1]=""
                    words[i]=nonterminal2+rb[:-1]
                    transform[index].append((nonterminal2,terminal))
            string=""
            for word in words:
                if word!="":
                    string+=word+" "
            outputTrees.write(string[:-1]+"\n")
            index+=1
        

        outputTrees.close()
        pickle.dump( transform, open( path+"lexicon.lex", "wb" ) )



    def __str__(self):
        pass


    def breakup(self, string,symbol):
        if symbol==string[0]:
            for i in xrange(len(string)):
                if string[i]!=symbol:
                    return (string[:i],string[i:])
        else:
            for i in xrange(len(string)):
                if string[i]==symbol:
                    return (string[:i],string[i:])
