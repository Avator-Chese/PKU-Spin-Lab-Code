# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 19:39:47 2016

@author: ppms
"""

import sqm
import sys
print(sys.argv)
if len(sys.argv)==1:

    fp=sys.argv[0]
    a=sqm.read_last_row(fp)
    print(a)
    #plotter=sqm.dynamic_plotter(fp,[])
    #print '0k'
    
else:
    fp=sys.argv[0]
    columns=sys.argv[1]
    plotter=sqm.dynamic_plotter(fp,columns)
    print('ok')
plotter.run()