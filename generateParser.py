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
    try:
        if sys.argv[1]=="test":
            name="test"
            treebank="test"
            comments="This parser was generated to test code"


    except:
        name=raw_input("What is the name of the parser?  :")
        treebank=raw_input("Which treebank do you want to use?  :")
        comments=raw_input("Any comments?  :")
    
    
    path="experiments/"+name+"/"    
    os.system("mkdir "+path[:-1])
    now=datetime.datetime.now()
    


    log=open(path+"log","w")
    log.write("++++Parser Information++++\n")
    log.write("name: "+name+"\n")
    log.write("based on treebank: "+treebank+"\n")
    log.write("time: "+str(now)+"\n")
    log.write("comments:\n"+comments+"\n")

    print "working..."
    os.system("notify-send \"building parsetable\"")

    os.system("./TOPify.py treebank/"+treebank+" "+path+"raw")


    lex=Lexicon()
    lex.extractFromTreebank(path+"raw",path)
    lex.save(path+"lexicon")
    pt=ParseTable()
    pt.generateFromTreeBank(path+"treebank")
    #pt.texfile(False,path)
    pt.csv(path)
    pt.save(path+"parsetable")
    
    
    log.write("++Parsetable Stats++\n")
    log.write(pt.stats())



    log.close()

    print "done!!!"
    
    os.system("notify-send \"Parsetable done.\"")
#-------------------------------
if __name__ == "__main__":
    main()
