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
from ParseTable import ParseTable
from Parser import Parser
from Lexicon import Lexicon

def main():

    lex=Lexicon(sys.argv[1],"wsj")
    
    pt=ParseTable()
    pt.generateFromTreeBank("wsj")
    pt.texfile(True)
    pt.save("test")


    #p=Parser(pt,lex)
    #p.parse(sys.argv[1])



#-------------------------------
if __name__ == "__main__":
    main()
