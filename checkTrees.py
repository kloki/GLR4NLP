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
def main():
    bad=[]
    for line in sys.stdin:
        if line.count("(")!=line.count(")"):
            bad.append(sys.stdin.index(line))
            
    if bad==[]:
        print "No trees are broken"
    else:
        print "These trees seems to be incorrect"
        print bad   

        

if __name__ == "__main__":
    main()
