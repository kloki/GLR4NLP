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
from __future__ import division
from Rule import Rule
from Item import Item

class CFG(object):
    """context free grammar
    """

    cfg={}
    terminals=[]
    nonTerminals=[]
    ruleIndex=0
    def __init__(self,textfile ):
        """
        Grammar rules are read from text file.
        
        A B C C C ...
        A = count of rule
        B = left hand side of rule
        C = right hand side of rule
        """
        
        with open(textfile,"r") as f:
            rules=f.readlines()
            for rule in rules:
                rule=rule.split()
                if len(rule)!=0:
                    self.addRule(rule[1],rule[2:],int(rule[0]))
                    self.checkSymbols(rule[1:])
        self.normaliseCounts()

    def addRule(self,lhs,rhs,count):
        """
        
        Arguments:
        - `lhs`:left hand side, string 
        - `rhs`:right hand side, list of string
        - `count`: count of rule, integer
        """
        if not lhs in self.cfg:
            self.cfg[lhs]=[Rule(lhs,rhs,count,self.ruleIndex)]
        else:
            self.cfg[lhs].append(Rule(lhs,rhs,count,self.ruleIndex))
        

        self.ruleIndex+=1
    
    def checkSymbols(self,symbolsList):
        """
        This function book keeps all terminals and non terminals
        """
        for symbol in symbolsList:
            if symbol[0].isupper():
                if symbol not in self.nonTerminals:
                    self.nonTerminals.append(symbol)
            else:
                if symbol not in self.terminals:
                    self.terminals.append(symbol)

    def normaliseCounts(self):
        """
        
        Arguments:
        - `self`:
        """
        for key,rules in self.cfg.iteritems():
            total=0
            for rule in rules:
                total+=rule.count
            for rule in rules:
                rule.count=rule.count/total

    def __str__(self):

        string=""
        for key,rules in self.cfg.iteritems():
            for rule in rules:
                string=string+str(rule)

        return string

    def rulesLHS(self,symbol):
        """
        Returns all rulesgiven a certain LHS
        """
        return self.cfg[symbol]


    def itemRulesLHS(self,symbol):
        """
        Returns all rules in the item format for the item set given a certain LHS
        """
        itemRules=[]
        for rule in self.cfg[symbol]:
            itemRules.append(Item(rule.lhs,rule.rhs,rule.count,0,"none",rule.index))
        return itemRules


    def listAllRules(self):
        rules=[]
        for values in self.cfg.itervalues():
            rules=rules+values
        return rules


    def getAllTerminals(self):
        return self.terminals[:]

    def getAllNonTerminals(self):
        return self.nonTerminals[:]
