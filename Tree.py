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
class Tree(object):
    treelets=[]
    def __init__(self):
        pass
    def __str__(self):
        string=""
        for i in self.treelets:
            string+=i+"\n"

        return string


    def addTreelet(self,treelet):
        self.treelets.append(treelet)


    def mergeTreelets(self,parent,nChildren):
        children=self.treelets[-nChildren:]
        self.treelets=self.treelets[:-nChildren]
        newTreelet="("+parent+" "
        for child in children:
            newTreelet+=child+" "
        newTreelet+=")"
        self.treelets.append(newTreelet)

    def getTreeString(self):
        return self.treelets[0]


    # this way == and != work with this object
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    
