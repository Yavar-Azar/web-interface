## all functions neeeded to analyze data 

from ase.io import read, write

import spglib



def cifanalyze(ciffile):
	cifdict={}
	temp=read(ciffile)


	textname=ciffile[:-3]+"txt"

	fn=open(textname, 'w')

	# list of elements
	elementlist = temp.get_chemical_symbols()
	unitcell  = temp.cell
	positions = temp.positions
	symbol = temp.symbols
	spgroup = spglib.get_spacegroup(temp)
	nat = len(elementlist)
 
	fn.write(ciffile+" data\n")
	fn.write("Number of atoms = "+str(nat)+"\n")
	fn.write("\nSpace Group based on SPGLIB = "+spgroup+"\n")

	fn.write("\n------------------------------------------\n")

	for idx, val in enumerate(elementlist):
		fn.write('{:s}{:8.4f}{:8.4f}{:8.4f}\n'.format(val, positions[idx,0], positions[idx,1], positions[idx,2]))
	fn.write("\n------------------------------------------\n")


	cifdict.update({"elements":elementlist})
	cifdict.update({"symbol":symbol})
	cifdict.update({"cell": unitcell})
	cifdict.update({"positions":positions})
	cifdict.update({"spgroup":spgroup})


	fn.close()

	return cifdict





def pwinpgen(ciffile, pseudodict, inp_data):
    """
    

    Parameters
    ----------
    ciffile : string
        name of cif file.
    pseudodict : dict
        dictionary containing pseudo files.

    Returns
    -------
    None.

    """
    
    test=read(ciffile)
    
    
    elementlist=test.get_chemical_symbols()
    
    
    pwiname=ciffile[:-3]+'pwi'
    pwoname=ciffile[:-3]+'pwo'
 
    
    
###  make pseudodict like this 
#
#    pseudodict={'Cs':'Cs.pbe-spn-rrkjus_psl.1.0.0.UPF',
#                'I':'I.pbe-n-rrkjus_psl.1.0.0.UPF',
#               'Pb':'Pb.pbe-dn-rrkjus_psl.1.0.0.UPF'}
    

## HERE WE CAN CHANGE INPUT PARAMETERS
    

    
    write(pwiname,test, input_data=inp_data, pseudopotentials=pseudodict, crystal_coordinates=True)     

    return
