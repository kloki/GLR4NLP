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

#scripts extract the flat sentences
import sys

def main():
    treebank=open(sys.argv[1],"r").readlines()
    if treebank[-1]!="\n":
        treebank+="\n"
     


    f=open(sys.argv[2],"w")
    
    for tree in treebank:
        sentence=""
        for p in tree.split():
            if ")" in p: 
                sentence+=p.replace(")","")+" "       
        f.write((sentence[:-1]+"\n"))
    f.close
#-------------------------------
if __name__ == "__main__":
    main()
