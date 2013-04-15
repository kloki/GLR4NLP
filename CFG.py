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
                if not rule=="":#ignore empty lines
                    rule=rule.split()
                    self.addRule(rule[1],rule[2:],int(rule[0]))
        
        self.normaliseCounts()
    

    def addRule(self,lhs,rhs,count):
        """
        
        Arguments:
        - `lhs`:left hand side, string 
        - `rhs`:right hand side, list of string
        - `count`: count of rule, integer
        """
        if not lhs in self.cfg:
            self.cfg[lhs]=[Rule(lhs,rhs,count)]
        else:
            self.cfg[lhs].append(Rule(lhs,rhs,count))
        
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

    def itemRulesLHS(self,symbol):
        """
        Returns all rules in the item format for the item set given a certain LHS
        """
        itemRules=[]
        for rule in self.cfg[symbol]:
            itemRules.append(Item(rule.lhs,rule.rhs,rule.count,0))
        return itemRules
