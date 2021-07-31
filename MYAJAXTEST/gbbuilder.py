#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 13:08:37 2021

@author: mmsg
"""

import json
from aimsgb import GrainBoundary, Grain, GBInformation





def gbbuilder(poscar, sigma, rotaxis, gbplane):
    """
    

    Parameters
    ----------
    poscar : string
        The initial structure file for grain boundary
    sigma : int
         A given Σ specifies the relation between the two grains
    rotaxis : list, optional
        The rotation axis of GB.
    gbplane : list, optional
        The GB plane for grain boundary. The default is [0,0,1].

    Returns
    -------
    None.

    """
    s = Grain.from_file(poscar)
    gb = GrainBoundary(rotaxis, sigma, gbplane, s)
    structure = gb.build_gb()
    structure.to(filename=poscar+".vasp",fmt="poscar")
    structure.to(filename=poscar+".cif",fmt="cif")
    ### !!! note that we have poscar as input and other formats should be converted to the poscar
    return


def axisdata(axis):
    """
    Parameters
    ----------
    axis : list
        rotation axis in list format for example [0,1,1].

    Returns
    -------
    info : dictionary
        information on the allowed sigma , angles and planes.

    """
    
    info = {}
    for sigma in range(3, 30, 2):
        try:
            info.update(GBInformation(axis, sigma, specific=True))
        except ValueError:
            pass

    ########   !!! note that info.keys are sigma 
    
      
       
    return info 



#####################################################################












