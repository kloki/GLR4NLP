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

class Node(object):
    index=0
    symbol="X"
    parent=0
    children=[]


    def __init__(self,index,symbol,parent,children):
        self.index=index
        self.symbol=symbol
        self.parent=parent
        self.children=children


    def addChild(self,child):
        self.children.append(child)
    

    def __str__(self):
        return str(self.index) +" "+self.symbol+" "+str(self.children)


    # this way == and != work with this object
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
