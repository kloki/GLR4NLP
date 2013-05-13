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
from CFG import CFG
from ParseTable import ParseTable
import cPickle as pickle

def main():
    rules={}
    actions={}
    gotos={}
    cfg=CFG("grammar/tomita")
    print cfg

    for rule in cfg.listAllRules():
            rules[rule.index]=rule
            print rule.probability

    terminals=cfg.getAllTerminals()
    nonTerminals=cfg.getAllNonTerminals()
    

    for i in xrange(13):
            actions[i]={}
            gotos[i]={}

            for t in terminals:
                actions[i][t]=[]
            actions[i]["$"]=[]#add endsymbol

            for nt in nonTerminals:
                gotos[i][nt]=[]
        
    
    actions[0]["det"]=["s3"]
    actions[0]["n"]=["s4"]
    actions[1]["prep"]=["s6"]
    actions[1]["$"]=["acc"]
    actions[2]["v"]=["s7"]
    actions[2]["prep"]=["s6"]
    actions[3]["n"]=["s10"]
    actions[4]["v"]=["r2"]
    actions[4]["prep"]=["r2"] 
    actions[4]["$"]=["r2"]
    actions[5]["prep"]=["r1"] 
    actions[5]["$"]=["r1"]
    actions[6]["det"]=["s3"]
    actions[6]["n"]=["s4"]
    actions[7]["det"]=["s3"]
    actions[7]["n"]=["s4"]
    actions[8]["prep"]=["r0"] 
    actions[8]["$"]=["r0"]
    actions[9]["v"]=["r4"]
    actions[9]["prep"]=["r4"] 
    actions[9]["$"]=["r4"]
    actions[10]["v"]=["r3"]
    actions[10]["prep"]=["r3"] 
    actions[10]["$"]=["r3"]
    actions[11]["v"]=["r5"]
    actions[11]["prep"]=["r5","s6"] 
    actions[11]["$"]=["r5"]
    actions[12]["prep"]=["r6","s6"] 
    actions[12]["$"]=["r6"]
    
        
    gotos[0]["NP"]=[2]
    gotos[0]["S"]=[1]
    gotos[1]["PP"]=[5]
    gotos[2]["PP"]=[9]
    gotos[2]["VP"]=[8]
    gotos[6]["NP"]=[11]
    gotos[7]["NP"]=[12]
    gotos[11]["PP"]=[9]
    gotos[12]["PP"]=[9]
    #printing
    string=""

    string+="ACTION TABLE\n"
    for i in actions.iterkeys():
        for j in actions[i].iterkeys():
            if actions[i][j]!=[]:
                for k in actions[i][j]:
                    string+="ACTION("+str(i)+","+j+")="+k+"\n"

    string+="\nGOTO TABLE\n"
    for i in gotos.iterkeys():
        for j in gotos[i].iterkeys():
            if gotos[i][j]!=[]:
                for k in gotos[i][j]:
                    string+="GOTO("+str(i)+","+j+")="+str(k)+"\n"
    print string

    #pickling
    pickle.dump( (actions,gotos,rules), open( "tomita.pt", "wb" ) )
#-------------------------------
if __name__ == "__main__":
    main()
