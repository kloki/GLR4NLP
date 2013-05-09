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

class Lexicon(object):
    transform={}
    def __init__(self):
        self.transform["i"]="n"
        self.transform["saw"]="v"
        self.transform["a"]="det"
        self.transform["man"]="n"
        self.transform["with"]="prep"
        self.transform["telescope"]="n"
        
    def transformWords(self,words):
        transformed=[]
        for word in words:
            transformed.append(self.transform[word])
        return transformed

    def getCategorie(self,word):
        return self.transform[word]

    def __str__(self):
        pass
