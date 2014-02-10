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
import math

class LexicalItem(object):
    symbol=""
    categories={}
    


    def __init__(self,symbol,categorie):
        self.symbol=symbol
        self.categories=categorie

    def __str__(self):
        string=""
        string+=self.symbol+"\n"
        for cat,prob in self.categories.iteritems():
            string+=cat+" "+str(prob)+"\n"
        return string
            
    def updateCategorie(self,categorie):
        if categorie not in self.categories:
            self.categories[categorie]=1
        else:
            self.categories[categorie]+=1

    def normalise(self):
        total=sum(self.categories.itervalues())
        for key in self.categories.keys():
            self.categories[key]=self.categories[key]/total
            
    def getMostLikely(self):
        categorie=""
        prob=0
        for cat,p in self.categories.iteritems():
            if p > prob:
                prob=p
                categorie=cat


        return categorie

    # this way == and != work with this object
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
