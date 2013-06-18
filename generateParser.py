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
    name=raw_input("What is the name of the parser?  :")
    path="experiments/"+name+"/"
    os.system("mkdir "+path[:-1])
    treebank=raw_input("Which treebank do you want to use?  :")
    comments=raw_input("Any comments?  :")
    now=datetime.datetime.now()
    log=open(path+"log","w")
    log.write("++++Parser Information++++\n")
    log.write("name: "+name+"\n")
    log.write("based on treebank: "+treebank+"\n")
    log.write("time: "+str(now)+"\n")
    log.write("comments:\n"+comments+"\n")

    lex=Lexicon()
    lex.extractFromTreebank("treebank/"+treebank,path)
    
    pt=ParseTable()
    pt.generateFromTreeBank(path+"treebank")
    pt.texfile(True,path)
    pt.save(path+"parseTable")





    log.close()



#-------------------------------
if __name__ == "__main__":
    main()
