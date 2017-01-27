import numpy as np
import simbad_reader
import ipdb

ipdb.set_trace()
target_list = simbad_reader.read_simbad('./secret/foo.txt')
ipdb.set_trace()

rands = 3600.*np.random.uniform(low=1.5,high=3.5,size=len(target_list))

np.savetxt('./secret/sep_limits.txt',rands,delimiter='\n',fmt='%05.0f')
