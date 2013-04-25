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
    """
    
    first={}
    def __init__(self,cfg,topSymbol):
        rules=cfg.rulesLHS(topSymbol)[:]
        usedRules=[]
        ##next we perform a closure like operation
        while len(rules)!=0:
            rule=rules[0]
            if rule.leftMostIsTerminal():
                self.addTerminal(rule.getLeftMost(),rule.lhs)
            else:
                newRules=cfg.rulesLHS(rule.getLeftMost())[:]
                for new in newRules:
                    if new not in usedRules:
                        rules.append(new)
            rules=rules[1:]
            usedRules.append(rule)
     


    def __str__(self):
        string=""
        for key ,terminals in self.first.iteritems():
            string=string+"FIRST("+key+")="+str(terminals)+"\n"
        return string
        
    def addTerminal(self,terminal, nonTerminal):
        """
        Add terminal to all items in list
        If nonterminal create new dictionary entry
        """
        for key in self.first.iterkeys():
            self.first[key].append(terminal)
        if not nonTerminal in self.first:
            self.first[nonTerminal]=[terminal]




    def appendDict(self,dictionary,key,element):
        if key in dictionary:
            dictionary[key].append(element)
        else:
            dictionary[key]=[element]
        return dictionary

    def getNonTerminals(self):
        return self.first.keys()

    def getTerminals(self,nonTerminal):
        return self.first[nonTerminal]

    # this way == and != work with this object
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
