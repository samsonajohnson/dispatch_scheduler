

import ipdb
import collections
import copy

def read_simbad(simbad_output):
    """
    make a dictionary of dictionaries for targets in the given list
    this is for the standard input of a simbad output file, and the 
    target dictionaries will have all the attributes in the file
    could probably be trimmed, but we'll see. might as well include all the 
    the information provided

    currently overwriting binaries, should look into a smarter way, based
    on visual versus spec possibly?
    """
    # open and read the simbad tsv
    with open(simbad_output,'r') as sb_file:
        lines  = sb_file.read().splitlines()
    key_list = []
    for raw_key in lines[5].split('\t'):
        key = "".join(raw_key.split()).lower()
        # some cases where i don't like the simbad key
        if key == '#': key = 'number'
        # i think it will be up to the user to figure which coord is which
        # and this allows for multiple ones to be used
        if 'coord' in key: key = key.split('(')[0]
        key_list.append(key)
    target_list = collections.OrderedDict()
    for target in lines[7:-3]:
        target_name = "".join(target.split('\t')[1].split())
        target_list[target_name] = collections.OrderedDict()
        ind = 0
        for key in key_list:
            spltarg = target.split('\t')

            if 'coord' in key:
                target_list[target_name][key] = collections.OrderedDict()
#                ra = " ".join(spltarg[ind].split()[0:3]).split()
#                ra = float(ra[0])*15.+float(ra[1])/60.+float(ra[2])/3600.
#                dec = " ".join(spltarg[ind].split()[3:]).split()
#                dec = float(dec[0])+float(dec[1])/60.+float(dec[2])/3600.
                target_list[target_name][key]['ra']=\
                    float(spltarg[ind].split()[0])
                target_list[target_name][key]['dec']=\
                    float(spltarg[ind].split()[1])
            else:
                # attempt to convert to a float, but don't throw if not
                try:
                    target_list[target_name][key] = \
                        float(target.split('\t')[ind])
                except:
                    target_list[target_name][key] = target.split('\t')[ind]
            ind+=1
        
    return target_list

def filter(target_list,decmin=None,decmax=None,ramin=None,\
               ramax=None,magv=None):
    """
    given a target list, go through and filter the list based on given limits
    if they are not the defaults provided. looking into adding more criteria
    """
    # a marker to see if we applied a filter
    new_list_flag = False
    new_list = {}


    # check for declination limits, will work this into setting up site 
    # most likely to be able to auto clip targets that will never rise
    # if so, throw a warning to user
    if not (decmin and decmax):
        new_list_flag = True
        if decmin and decmax:
            for key in target_list:
                if target_list[key]['coord1']['dec']>decmin and \
                        target_list[key]['coord1']['dec']<decmax :
                    new_list[key]=\
                        copy.deepcopy(target_list[key])
        elif decmin:
            for key in target_list:
                if target_list[key]['coord1']['dec']>decmin:
                    new_list[key]=\
                        copy.deepcopy(target_list[key])
        elif decmax:
            for key in target_list:
                if target_list[key]['coord1']['dec']<decmax:
                    new_list[key]=\
                        copy.deepcopy(target_list[key])

    # check for RA limits, this is weird but why not include the option
    if not (ramin and ramax):
        new_list_flag = True
        if ramin and ramax:
            for key in target_list:
                if target_list[key]['coord1']['ra']>ramin and \
                        target_list[key]['coord1']['ra']<ramax :
                    new_list[key]=\
                        copy.deepcopy(target_list[key])
        elif ramin:
            for key in target_list:
                if target_list[key]['coord1']['ra']>ramin:
                    new_list[key]=\
                        copy.deepcopy(target_list[key])
        elif ramax:
            for key in target_list:
                if target_list[key]['coord1']['ra']<ramax:
                    new_list[key]=\
                        copy.deepcopy(target_list[key])
    return new_list

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    tlist = read_simbad('sample_list.txt')
    ipdb.set_trace()
    newlist = filter(tlist,decmax=30.)
    ras = []
    decs = []
    for key in newlist.keys(): ras.append(newlist[key]['coord1']['ra'])
    for key in newlist.keys(): decs.append(newlist[key]['coord1']['dec'])
    plt.plot(ras,decs,'.')
    plt.show()
    ipdb.set_trace()
