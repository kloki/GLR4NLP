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

import sys
import os
import datetime
from ParseTable import ParseTable
from Parser import Parser
from Lexicon import Lexicon

def main():
    parserName=sys.argv[1]
    corpusName=sys.argv[2]
    pt=ParseTable()
    lex=Lexicon()
    print "loading parsetable....."
    pt.load("experiments/"+parserName+"/parsetable.pt")
    lex.load("experiments/"+parserName+"/lexicon.lex")
    print "done"
    p=Parser(pt,lex)
    corpus=open(corpusName,"r").readlines()
    if corpus[-1]=="\n":
        corpus=corpus[:-1]
    for line in corpus:
         print line
         p.parse(line)
         


#-------------------------------
if __name__ == "__main__":
    main()
