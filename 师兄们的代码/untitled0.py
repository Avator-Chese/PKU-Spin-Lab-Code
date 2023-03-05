# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 19:39:47 2016

@author: ppms
"""

import sqm
import sys
if len(sys.argv)==2:
    fp=sys.argv[1]
    plotter=sqm.dynamic_plotter(fp,[])
else:
    fp=sys.argv[1]
    columns=sys.argv[2]
    plotter=sqm.dynamic_plotter(fp,columns)
plotter.run()