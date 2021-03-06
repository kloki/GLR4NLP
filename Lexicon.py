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

#import cPickle as pickle
import pickle 
from LexicalItem import LexicalItem
class Lexicon(object):
    
    lexicon={}
    def __init__(self):
        pass

    def extractFromTreebank(self,treebankName,path):
    
        """
        extracts the lexical words from tree bank and stores them.
        Also creates a sanatized treebank
        """
        f=open(treebankName,"r")
        treebank=f.read()
        f.close()

        #some sanitizing
        # treebank=treebank.replace(" (, ,)","") 
        # treebank=treebank.replace(" (. .)","")
        # treebank=treebank.replace(" (. ?)","")
        # treebank=treebank.replace(" (. !)","")
        # treebank=treebank.replace(" (\" \")","")
        # treebank=treebank.replace(" (' ')","")
        # treebank=treebank.replace(" ('' '')","")
        # treebank=treebank.replace(" (`` ``)","")
        # treebank=treebank.replace(" (; ;)","")
        # treebank=treebank.replace(" (: :)","")
        trees=treebank.split("\n")
        outputTrees=open(path+"treebank","w")
        for tree in trees:
            words=tree.split()
            for i in xrange(len(words)):
                if ")" in words[i]:
                    (lb,nonterminal)=self.breakup(words[i-1],"(")
                    (terminal,rb)=self.breakup(words[i],")")
                    nonterminal2=nonterminal.lower()
                    words[i-1]=""
                    words[i]=nonterminal2+rb[:-1]
                    self.updateLexicon(terminal,nonterminal)
            string=""
            for word in words:
                if word!="":
                    string+=word+" "
            outputTrees.write(string[:-1]+"\n")
        

        outputTrees.close()

        for key in self.lexicon.keys():
            self.lexicon[key].normalise()
       

    def load(self,filename):
        templex=pickle.load(open(filename,"rb"))
        self.lexicon={} 
        for word,categories in templex.items():
            self.lexicon[word]=LexicalItem(word,categories)
        


    def save(self,path):
        """
        Removing object in data structure
        dict[word]=lexicalitem
        dict[word]={categoriedict}
        """
        templex={}
        for word in self.lexicon.keys():
            
            templex[word]=self.lexicon[word].categories

        
        lf= open( path+".lex", "wb" )
        pickle.dump( templex, lf )
        lf.close()
        
    
    
    def __str__(self):
        string=""
        for key in self.lexicon.keys():
            string+=str(self.lexicon[key])+"\n"
        
        return string


    def updateLexicon(self,terminal,nonterminal):
        if terminal not in self.lexicon:
            self.lexicon[terminal]=LexicalItem(terminal,{nonterminal:1})
        else:
            self.lexicon[terminal].updateCategorie(nonterminal)



    def breakup(self, string,symbol):
        if symbol==string[0]:
            for i in xrange(len(string)):
                if string[i]!=symbol:
                    return (string[:i],string[i:])
        else:
            for i in xrange(len(string)):
                if string[i]==symbol:
                    return (string[:i],string[i:])



    def getCategories(self,words):
        categories=[]
        for word in words:
            if word not in self.lexicon:
                categories.append("nn")
            else:
                categories.append(self.lexicon[word].getMostLikely().lower())



        return categories
