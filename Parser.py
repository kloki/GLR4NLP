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
from ParsePath import ParsePath
class Parser(object):
    paths=[]
    words=[]
    categories=[]
    lookaheads=[]
    def __init__(self,pt,lex):
        self.parseTable=pt
        self.lexicon=lex

    def parse(self, sentence):


        self.words=sentence.split()
        self.categories=self.lexicon.transformWords(self.words)
        self.lookaheads=self.categories[:]
        #start parsing
        self.paths.append(ParsePath("S0"))

        while True:
            self.retrieveStates()
            self.
        




    def shift(self):
        pass

    def reduce(self):
        pass

    def __str__(self):
        pass
