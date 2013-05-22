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

class First(object):
    """
    Contains all the first terminals for an itemset.
    It is simplified as it assumes that the grammar does not contain a mapping to an empty RHS
    
    Add the moment is not very efficient but I wanted to keep it seperate from the ItemSet generation


    Needs reworking

      S
     / \
    NP VP

    VP wont be parsed
    """
    
    first={}
    def __init__(self,cfg,topSymbol):

        #First in initialize the First Set on the top symbol
        self.first=self.findFirstTerminals(topSymbol,cfg)




        ##We might miss some nonTerminals so we have to check them all This could be more efficient
        nonTerminals=cfg.getAllNonTerminals()
        while nonTerminals!=[]:
            symbol=nonTerminals.pop(0)
            if symbol not in self.first.keys():
                newFirst=self.findFirstTerminals(symbol,cfg)
                self.mergeWithMain(newFirst)

    def mergeWithMain(self,newFirst):
        oldkeys=self.first.keys()
        newkeys=newFirst.keys()
        for key in newkeys:
            if key not in oldkeys:
                self.first[key]=newFirst[key]



    def findFirstTerminals(self,symbol,cfg):
        rules=cfg.rulesLHS(symbol)[:]
        usedRules=[]
        firstDictionary={}
        firstDictionary[symbol]=[]
        ##next we perform a closure like operation starting with the given symbol
        while len(rules)!=0:
            rule=rules[0]
            #if new symbol create entry
            if rule.lhs not in firstDictionary.keys():
                firstDictionary[rule.lhs]=[]
            if rule.leftMostIsTerminal():
                firstDictionary=self.addTerminal(firstDictionary,rule.getLeftMost(),rule.lhs)
            else:
                newRules=cfg.rulesLHS(rule.getLeftMost())[:]
                for new in newRules:
                    if new not in usedRules:
                        rules.append(new)
            rules=rules[1:]
            usedRules.append(rule)
        return firstDictionary

    def __str__(self):
        string=""
        for key ,terminals in self.first.iteritems():
            string=string+"FIRST("+key+")="+str(terminals)+"\n"
        return string
        
    def addTerminal(self, dictionary,terminal, nonTerminal):
        """
        Add terminal to all items in list
        """
        for key in dictionary.iterkeys():
            if terminal not in dictionary[key]:
                dictionary[key].append(terminal)
            
        return dictionary
    


    def getNonTerminals(self):
        return self.first.keys()

    def getTerminals(self,symbol):
        if symbol.isupper():
            return self.first[symbol][:]
        else:
            return [symbol]
    # this way == and != work with this object
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
