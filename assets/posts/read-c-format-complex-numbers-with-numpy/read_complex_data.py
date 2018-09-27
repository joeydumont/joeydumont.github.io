# ------------------------------- Information ------------------------------- #
# Author:       Justine Pepin                  <justine.pepin@emt.inrs.ca>    #
# Created:      2018-07-35                                                    #
# Description:  Tries to read complex numbers written in the C++ format from  #
#               a file.                                                       #
# --------------------------------------------------------------------------- #

# -- Import modules
import numpy as np

# -- We try the obvious way of reading the data.
invalid_data = np.genfromtxt("rand_test.txt",dtype=complex)

print(invalid_data)

# -- When that doesn't work, we get fancy and manually convert the data to
# -- the proper datatype.
def LoadComplexData(file,**genfromtxt_args):
  complex_parser = np.vectorize(lambda x: complex(*eval(x)))
  return complex_parser(np.genfromtxt(file,dtype=str,**genfromtxt_args))

valid_data = LoadComplexData("rand_test.txt")

print(valid_data)
